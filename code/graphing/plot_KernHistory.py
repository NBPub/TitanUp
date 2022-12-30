import pandas as pd
# import numpy as np
from pathlib import Path
# import json

from plot_KernHistory_scripts import punt_att, year_boxen, punt_distance_reg,\
                        xPA_reg, binary_reg

    # Part 1 - Kern vs NFL 2009-2021, only punts as a Titan
p = Path(Path.cwd(), 'processed data')
# Gather all punt data 2009-2021
punts = pd.read_parquet(Path(p,'TN_punts_2009-2021.parquet'))
others = pd.read_parquet(Path(p,'notTN_punts_2009-2021.parquet'))
punts = pd.concat([punts,others])
punts.reset_index(drop=True, inplace=True)

# ensure datatypes
for val in ['yardline_100','punt_blocked','punt_inside_twenty','punt_in_endzone','punt_out_of_bounds',
            'punt_downed','punt_fair_catch','kick_distance','net_yards','punt_returned']:
    punts.loc[:,val] = punts[val].astype(int)

# mark Kern for plots, lump everyone else together    
punts.loc[punts[punts.punter_player_name != 'B.Kern'].index, 'punter_player_name'] = 'Rest of NFL'
 

# # Punt Attempts vs Yds to go (KDE+bars)
punt_att(punts, (2017,2020))    

# OOB/YTG vs year and Net/YTG vs year, boxen
year_boxen(punts,'punt_out_of_bounds',(2014,2022))
year_boxen(punts,'net_yards',(2016,2022))

    # LM Plots
# Big Binary Regressions
sub = punts.loc[:,['yardline_100','season','punter_player_name', 
                   'punt_inside_twenty','touchback','punt_out_of_bounds', 
                   'punt_downed','punt_fair_catch']]
binary_reg(sub)
del sub

# Punt Distance Regressions
punt_distance_reg(punts.loc[:,['yardline_100','season','punter_player_name', 
                               'kick_distance','net_yards']])

# EPA/WPA Regressions
xPA_reg(punts.loc[:,['yardline_100','season','punter_player_name', 'epa','wpa']])

Return rate vs YTG comes from other plot_Punts


