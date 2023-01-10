import pandas as pd
import numpy as np
from pathlib import Path
import json

from plot_Punts_scripts import punt_att, punt_distance_bar, OOB_bar, two_bar, \
                        epa_bar, binary_LogReg, KernReturn_LogReg,\
                        NormDist_RetRate_historical, punt_distance_reg_order
                        
###     NOTE! Saves to three different folders!     ###
        # graphs/ Intro, Kern History, Kern v Stonehouse 

    # Part 0 - Punt plots with all NFL data
p = Path(Path.cwd(), 'processed data')
# Gather all punt data 2009-2021
punts = pd.read_parquet(Path(p,'TN_punts_2009-2021.parquet'))
others = pd.read_parquet(Path(p,'notTN_punts_2009-2021.parquet'))
punts = pd.concat([punts,others])
punts.reset_index(drop=True, inplace=True)
# add in 2022 punts
others = pd.read_parquet(Path(p,'punts_2022.parquet'))
punts = pd.concat([punts,others])
punts.reset_index(drop=True, inplace=True)
# ensure datatypes
for val in ['yardline_100','punt_blocked','punt_inside_twenty','punt_in_endzone','punt_out_of_bounds',
            'punt_downed','punt_fair_catch','kick_distance','net_yards','punt_returned']:
    punts.loc[:,val] = punts[val].astype(int)
 


p = Path(Path.cwd(), 'processed data', 'percentiles_other_2022.json')
with open(p, 'r') as file:
    measures = json.loads(file.read())
check = measures.pop('check')
punters = measures.pop('punters')
teams = measures.pop('teams')
# measures = {key:np.array(val) for key,val in measures.items()} 
del measures


# Order justification for Net/Gross Yds vs Yds to go fit
punt_distance_reg_order(punts,'net_yards')
punt_distance_reg_order(punts,'kick_distance')

# Punt Attempts vs Yds to go (KDE+bars)
punt_att(punts.yardline_100)    
    
# Net/Gross Yds vs Yds to go (bar), with and without proportional lines marked
punt_distance_bar(punts, False)
punt_distance_bar(punts, True)

# OOB vs Yds to go (bar). Single
OOB_bar(punts)
# EPA vs Yds to go (bar). Single.
epa_bar(punts) 

# Touchback, Downed vs Yds to go (bar). 2x1
two_bar(punts,['touchback','punt_downed'],0.45, 'bar_TB-Downed.png')
# Fair Catch, Inside Twenty vs Yds to go (bar). 2x1
two_bar(punts,['punt_fair_catch','punt_inside_twenty'],1, 'bar_FC-In20.png')


    # Logistic Regressions, subset of data for easier calculations
sub = punts[(punts.yardline_100<91) & (punts.yardline_100>39)]

# Binary, two groups
binary_LogReg(sub, ['punt_inside_twenty', 'punt_fair_catch'])
binary_LogReg(sub, ['punt_out_of_bounds', 'touchback', 'punt_downed'])

# Kern vs NFL, 2021 and prior with cutoff year for two Kerns. doesn't change with 2022 updates
# KernReturn_LogReg(sub, 2016, 'punt_out_of_bounds')
# KernReturn_LogReg(sub, 2016, 'punt_returned')



# Normalized Net yards vs Return Rate for punter seasons (scatter + reg)
test = pd.DataFrame(columns = ['name','season','return_rate', 'norm_net'])
k = 1
for val in punts.punter_player_name.unique():
    sub = punts[punts.punter_player_name == val]
    for year in sub.season.unique():
        sub2 = sub[sub.season == year]
        if sub2.shape[0] > 30: # 30 PUNT MINIMUM FOR PUNTER FOR SEASON
            test.loc[k,'name'] = val
            test.loc[k,'season'] = year
            test.loc[k,'punts'] = int(sub2.shape[0])
            test.loc[k,'return_rate'] = sub2.punt_returned.mean()
            test.loc[k,'norm_net'] = np.mean(sub2.net_yards/sub2.yardline_100)
            test.loc[k,'norm_gross'] = np.mean(sub2.kick_distance/sub2.yardline_100)
            k+=1
test.punts = test.punts.astype('int')
test['return_rate'] = test['return_rate'].astype('float')
test['norm_net'] = test['norm_net'].astype('float')
test['norm_gross'] = test['norm_gross'].astype('float')

NormDist_RetRate_historical(test, 'norm_net')
NormDist_RetRate_historical(test, 'norm_gross')
