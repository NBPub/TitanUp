import pandas as pd
# import numpy as np
from pathlib import Path
import json

from plot_KernStone_scripts import punt_att_KDE, punt_distance_boxen,\
                    punt_distance_reg, epa_reg, binaries_reg


    # Part II - Stonehouse vs Kern Plots
p = Path(Path.cwd(), 'processed data')
stone = pd.read_parquet(Path(p,'punts_2022.parquet'))   
kern = pd.read_parquet(Path(p,'TN_punts_2009-2021.parquet'))   


p = Path(Path.cwd(), 'processed data', 'percentiles_other_2022.json')
with open(p, 'r') as file:
    measures = json.loads(file.read())
check = measures.pop('check')
punters = measures.pop('punters')
teams = measures.pop('teams')
# measures = {key:np.array(val) for key,val in measures.items()} 
del measures

kern = kern[kern.punter_player_id == punters['B.Kern']] # Kern --> only Kern punts
kern = kern[(kern.season > 2016) & (kern.season < 2020)]  # Kern --> only 2017-2019
stone = stone[stone.punter_player_id == punters['R.Stonehouse']] # Stone --> only Stonehouse punts
punts = pd.concat([kern,stone])
del kern,stone


# Punt Attempts vs Yds to go (KDE)
punt_att_KDE(punts)    
    
# Net/Gross Yds vs Yds to go (boxen)
punt_distance_boxen(punts)
    
# Net/Gross Yds vs Yds to go (LM plot)
punt_distance_reg(punts)
# EPA vs Yds to go (LM plot)
epa_reg(punts)
# Binary Metrics vs Yds to go (LM plot)
binaries_reg(punts.loc[:,['yardline_100','season','punter_player_name', 
  'punt_inside_twenty','touchback','punt_out_of_bounds','punt_downed','punt_fair_catch',
                 ]])