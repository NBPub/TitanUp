import pandas as pd
import numpy as np
from pathlib import Path
import json

from plot_Stone2022_scripts import punt_att_KDE, punt_att_swarm,\
                    punt_distance_boxen, punt_distance_reg,\
                    individual_punter_reg

# load team_colors
teamcolors = pd.read_csv(Path(Path.cwd(),'pbp data', 'teamcolors.csv'))
teamcolors.set_index('team',inplace=True,drop=True)
teamcolors.loc['NYJ','color3'] = '#adadad'
teamcolors.loc['NYJ','color4'] = '#000000'
    
    # Part III - Stonehouse 2022 plots
p = Path(Path.cwd(), 'processed data','punts_2022.parquet')
punts = pd.read_parquet(p)   
analyze = 'R.Stonehouse'
punts.loc[punts[punts.punter_player_name=='R.Stonehouse'].index,'POI'] =analyze
punts.loc[punts[punts.punter_player_name!='R.Stonehouse'].index,'POI'] ='Rest of NFL'

p = Path(Path.cwd(), 'processed data', 'percentiles_other_2022.json')
with open(p, 'r') as file:
    measures = json.loads(file.read())
check = measures.pop('check')
punters = measures.pop('punters')
teams = measures.pop('teams')
# measures = {key:np.array(val) for key,val in measures.items()} 
del measures

# Punter Attempts across League (boxen + swarm)
punt_att_swarm(punts, teams, 'R.Stonehouse')
    
# Punt Attempts vs Yds to go (KDE)
punt_att_KDE(punts)    
    
# Net/Gross Yds vs Yds to go (boxen)
punt_distance_boxen(punts, 'R.Stonehouse')
    
# Net/Gross Yds vs Yds to go (LM plot)
punt_distance_reg(punts)

# Individual Punter Plots
test = pd.DataFrame()
k = 1
for val in punts.punter_player_name.unique():
    sub = punts[punts.punter_player_name == val]
    if sub.shape[0] >= 30: # 30 PUNT MINIMUM FOR PUNTER FOR SEASON
        test.loc[k,'name'] = val
        test.loc[k,'team'] = teams[val]
        test.loc[k,'color'] = teamcolors['color'][teams[val]]
        test.loc[k,'c2'] = teamcolors['color2'][teams[val]]
        test.loc[k,'c3'] = teamcolors['color3'][teams[val]]
        test.loc[k,'c4'] = teamcolors['color4'][teams[val]]
        test.loc[k,'punts'] = int(sub.shape[0])
        test.loc[k,'return_rate'] = sub.punt_returned.mean()
        test.loc[k,'norm_net'] = np.mean(sub.net_yards/sub.yardline_100)
        test.loc[k,'norm_gross'] = np.mean(sub.kick_distance/sub.yardline_100)
        test.loc[k,'YTG'] = np.mean(sub.yardline_100)
        test.loc[k,'touchback'] = np.mean(sub.touchback)
        test.loc[k,'in20'] = np.mean(sub.punt_inside_twenty)
        test.loc[k,'OOB'] = np.mean(sub.punt_out_of_bounds)
        k+=1
test.punts = test.punts.astype('int')
test['return_rate'] = test['return_rate'].astype('float')
test['norm_net'] = test['norm_net'].astype('float')
test['norm_gross'] = test['norm_gross'].astype('float')
test['YTG'] = test['YTG'].astype('float')
test['touchback'] = test['touchback'].astype('float')
test['in20'] = test['in20'].astype('float')
test['OOB'] = test['OOB'].astype('float')

# Net vs Returns
individual_punter_reg(test, 'return_rate', 'norm_net', 'stonehouse_nfl_norm-net_vs_return-rate.png')

# Gross vs Returns
individual_punter_reg(test, 'return_rate', 'norm_gross', 'stonehouse_nfl_norm-gross_vs_return-rate.png')

# Returns vs YTG
individual_punter_reg(test, 'YTG', 'return_rate', 'stonehouse_nfl_return-rate_vs_ytg.png')

# OOB vs YTG
individual_punter_reg(test, 'YTG', 'OOB', 'stonehouse_nfl_OOB_vs_ytg.png')
    
# In20 vs YTG
individual_punter_reg(test, 'YTG', 'in20', 'stonehouse_nfl_in20_vs_ytg.png')
    
    


