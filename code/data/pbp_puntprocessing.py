from pathlib import Path
import pandas as pd
import numpy as np
import json


punt_cols = ["play_id", "game_id", "home_team", "away_team", "posteam", "defteam", "game_date",
            "yardline_100", "yrdln", "desc", "play_type", "ydstogo", "touchback",
            "kick_distance", "ep", "epa", "wp", "wpa", "punt_blocked", "punt_inside_twenty",
            "punt_in_endzone","punt_out_of_bounds", "punt_downed", "punt_fair_catch",
            "punt_attempt", "punter_player_id", "punter_player_name", "punt_returner_player_id",
            "punt_returner_player_name", "return_yards", "season", "season_type", "week",
            "touchdown", "td_team", "temp", "roof"]
p = Path(Path.cwd(), 'pbp data','play_by_play_2022.parquet')
data = pd.read_parquet(p)

# Gather punt data, list of punters
punts = data.loc[data[data.punt_attempt==1].index, punt_cols] # could check "play column"
# Gather dictionary of names / ids
punters = {} # id:name
teams = {} # name:team
for val in punts.punter_player_name.unique():
    if val:
        punters[val] = punts[punts.punter_player_name == val].punter_player_id.unique()[0]
        team = punts[punts.punter_player_name == val].posteam.unique()
        if team.shape[0] > 1:
            print('multiple teams for', val, team) 
        teams[val] = team[0]
        

# Data Cleaning Functions
# punter name and id to null punts, seems to be for blocked punts
for val in punts[punts.punter_player_name.isnull()].index:
    fill_name = punts.loc[val,'desc'].split('-')[1].split(' ')[0]
    if fill_name in punters.keys():
        punts.loc[val, 'punter_player_name'] = fill_name
        punts.loc[val, 'punter_player_id'] = punters[fill_name]
    else:
        print(val, 'not filled')

# add kick_distance to touchbacks
punts.loc[punts[punts.kick_distance.isnull()].index,'kick_distance'] = punts[punts.kick_distance.isnull()].yardline_100-20

# add net yards: kick_distance - return yards
punts.loc[:,'net_yards'] = punts.kick_distance - punts.return_yards

# add return binary
punts.loc[:,'punt_returned'] = 0
punts.loc[punts[(punts.punt_fair_catch == 0)&(punts.punt_blocked == 0)&\
                (punts.punt_out_of_bounds == 0)&(punts.punt_downed == 0)&\
                (punts.touchback == 0)].index,'punt_returned'] = 1

# change columns to int to save space
for val in ['yardline_100','punt_blocked','punt_inside_twenty','punt_in_endzone','punt_out_of_bounds',
            'punt_downed','punt_fair_catch','kick_distance','net_yards', 'punt_returned']:
    punts.loc[:,val] = punts[val].astype(int)


# save punts
punts.to_parquet(Path(Path.cwd(), 'processed data','punts_2022.parquet'))

    # PUNTERS ALSO DID
player_id_cols = []
for val in data.columns:
    for tackle_key in ['solo_tackle_', 'assist_tackle_', 'tackle_with_assist_', 'tackle_for_loss']:
        if val.startswith(tackle_key) and val.endswith('player_id'):
            player_id_cols.append(val)

player_id_cols.append('passer_player_id') # all passess
player_id_cols.append('rusher_id') # Rush something about scrambles
player_id_cols.append('receiver_player_id') # all targets

# Others, will have to find punter name later, print desc for hints
test = pd.DataFrame()
check = []
print('Punters also did:')
for val in punters.values():
    for col in player_id_cols:
        if data[data[col] == val].shape[0] > 0:
            if col not in check:
                check.append(col)
                print('\t',col)
            test = pd.concat([test, data[data[col] == val]])
            
# save punter other dataframe
test.to_parquet(Path(Path.cwd(), 'processed data','punts_other_2022.parquet'))


# calculate percentiles for EPA distributions
measures = {}
measures['pass_epa'] = np.percentile(data[(data.pass_attempt == 1) & (data.qb_epa.notnull())].qb_epa,range(1,100))
measures['rush_epa'] = np.percentile(data[(data.rush == 1) & (data.epa.notnull())].epa,range(1,100))
measures['rec_epa'] = np.percentile(data[(data.receiver_player_id.notnull()) & (data.epa.notnull())].epa,range(1,100))

# save percentiles, check list, punter ID dict, punter team dict
m2 = {key:val.tolist() for key,val in measures.items()}
m2['check'] = check
m2['punters'] = punters
m2['teams'] = teams
with open(Path(Path.cwd(), 'processed data','percentiles_other_2022.json'), 'w', encoding='utf-8') as file:
    file.write(json.dumps(m2))
    
del data, punts, test

