import pandas as pd
# import numpy as np
from pathlib import Path

# Iterate through pbp dataframes
#   collect other  punt data in notTN_punts.parquet 

# load existing
p = Path(Path.cwd(), 'processed data')
if Path(p,'notTN_punts.parquet').exists():
    notTN_punts = pd.read_parquet(Path(p,'notTN_punts.parquet'))
else:
    notTN_punts = pd.DataFrame()

# Data to keep for punts
punt_cols = ["play_id", "game_id", "home_team", "away_team", "posteam", "defteam", "game_date",
            "yardline_100", "yrdln", "desc", "play_type", "ydstogo", "touchback",
            "kick_distance", "ep", "epa", "wp", "wpa", "punt_blocked", "punt_inside_twenty",
            "punt_in_endzone","punt_out_of_bounds", "punt_downed", "punt_fair_catch",
            "punt_attempt", "punter_player_id", "punter_player_name", "punt_returner_player_id",
            "punt_returner_player_name", "return_yards", "season", "season_type", "week",
            "touchdown", "td_team", "temp", "roof"]

for year in range(2009,2023): # 2009 - 2023 total dataset
    URL = f'https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_{year}.parquet'
    data = pd.read_parquet(URL)
    
    # Titans Punts
    punts = punts = data.loc[data[data.punt_attempt==1].index, punt_cols]
 
    # ID:Name of Punters
    punters = {} # id:name
    for val in punts.punter_player_name.unique():
        if val:
            punters[val] = punts[punts.punter_player_name == val].punter_player_id.unique()[0] 
 
    # Data Cleaning Functions
    # punter name and id to null punts, seems to be for blocked punts as shown above
    for val in punts[punts.punter_player_name.isnull()].index:
        fill_name = punts.loc[val,'desc'].split('-')[1].split(' ')[0]
        if fill_name in punters.keys():
            punts.loc[val, 'punter_player_name'] = fill_name
            punts.loc[val, 'punter_player_id'] = punters[fill_name]
        else:
            print(val, 'not filled')
    
    # remove B.Kern and R.Stonehouse   
    punts=punts[~punts.punter_player_name.isin(['B.Kern','R.Stonehouse'])]
    
    # add kick_distance to touchbacks
    punts.loc[punts[punts.kick_distance.isnull()].index,'kick_distance'] = punts[punts.kick_distance.isnull()].yardline_100-20
    
    # add net yards: kick_distance - return yards
    punts.loc[:,'net_yards'] = punts.kick_distance - punts.return_yards
    
    # save punts
    try:
        notTN_punts = pd.concat([notTN_punts, punts])
        print('Added', year, 'to punts.')
    except Exception as e:
        print('error for', year, str(e))

notTN_punts.dropna(subset='punter_player_name', inplace=True) # don't care about a few missing
notTN_punts.to_parquet(path=Path(p,'notTN_punts.parquet'))




    # Post Processing Adjustments
# Add punt_returned binary metric for returnable punts
# Change cols to int to save space
# 
# for file in ['notTN_punts_2009-2021.parquet', 'TN_punts_2009-2021.parquet', 'punts_2022.parquet']:
#     punts = pd.read_parquet(Path(p,file))
#     punts.loc[:,'punt_returned'] = 0
#     punts.loc[punts[(punts.punt_fair_catch == 0)&(punts.punt_blocked == 0)&\
#                     (punts.punt_out_of_bounds == 0)&(punts.punt_downed == 0)&\
#                     (punts.touchback == 0)].index,'punt_returned'] = 1
#     for val in ['yardline_100','punt_blocked','punt_inside_twenty','punt_in_endzone','punt_out_of_bounds',
#                 'punt_downed','punt_fair_catch','kick_distance','net_yards', 'punt_returned']:
#         punts.loc[:,val] = punts[val].astype(int)
    
#     punts.to_parquet(Path(p,file))












