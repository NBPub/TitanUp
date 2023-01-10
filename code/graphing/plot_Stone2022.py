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


p = Path(Path.cwd(), 'processed data', 'percentiles_other_2022.json')
with open(p, 'r') as file:
    measures = json.loads(file.read())
check = measures.pop('check')
punters = measures.pop('punters')
teams = measures.pop('teams')
# measures = {key:np.array(val) for key,val in measures.items()} 
del measures

# FIX LA --> LAR
# teamcolors.rename(index = {'LA':'LAR'}, inplace=True)
# teamcolors.drop_duplicates(inplace=True)
teamfix = [punter for punter in teams if teams[punter] =='LA']
for punter in teamfix:
    teams[punter] = 'LAR'


# Punter Attempts across League (boxen + swarm)
# better to just figure out on jupyter
punt_att_swarm(punts, teams, 'R.Stonehouse')
    
# Punt Attempts vs Yds to go (KDE)
punt_att_KDE(punts, ['R.Stonehouse'])
punt_att_KDE(punts, ['M.Wishnowsky', 'T.Townsend'])
# punt_att_KDE(punts, 'T.Townsend')       

    
# Net/Gross Yds vs Yds to go (boxen)
punt_distance_boxen(punts, 'R.Stonehouse')
    
# Net/Gross Yds vs Yds to go (LM plot)
punt_distance_reg(punts, 'R.Stonehouse')

# Individual Punter Plots
test = pd.DataFrame()
k = 1
for val in punts.punter_player_name.unique():
    sub = punts[punts.punter_player_name == val]
    if sub.shape[0] >= 30: # 30 PUNT MINIMUM FOR PUNTER FOR SEASON
        test.loc[k,'name'] = val
        test.loc[k,'team'] = teams[val]
        test.loc[k,'color'] = teamcolors.loc[teams[val], 'color']
        test.loc[k,'c2'] = teamcolors.loc[teams[val], 'color2']

        
        test.loc[k,'punts'] = int(sub.shape[0])
        test.loc[k,'return_rate'] = sub.punt_returned.mean()
        test.loc[k,'norm_net'] = np.mean(sub.net_yards/sub.yardline_100)
        test.loc[k,'norm_gross'] = np.mean(sub.kick_distance/sub.yardline_100)
        test.loc[k,'YTG'] = np.mean(sub.yardline_100)
        test.loc[k,'touchback'] = np.mean(sub.touchback)
        test.loc[k,'in20'] = np.mean(sub.punt_inside_twenty)
        test.loc[k,'OOB'] = np.mean(sub.punt_out_of_bounds)
        test.loc[k,'downed'] = np.mean(sub.punt_downed)
        test.loc[k,'FC'] = np.mean(sub.punt_fair_catch)
        test.loc[k,'net'] = np.mean(sub.net_yards)
        test.loc[k,'gross'] = np.mean(sub.kick_distance)
        k+=1
        
test.punts = test.punts.astype('int')
for val in ['return_rate','norm_net','norm_gross','YTG','touchback','in20',
            'OOB','downed','FC','net','gross']:
    test[val] = test[val].astype('float')




# Net vs Returns, specify (data, x,y, savename)
individual_punter_reg(test, 'return_rate', 'norm_net', 'norm-net_vs_return-rate.png', True)

# Gross vs Returns
individual_punter_reg(test, 'return_rate', 'norm_gross', 'norm-gross_vs_return-rate.png', True)

# Returns vs YTG
individual_punter_reg(test, 'YTG', 'return_rate', 'return-rate_vs_ytg.png', True)

    # others
# OOB vs YTG
individual_punter_reg(test, 'YTG', 'OOB', 'extra/OOB_vs_ytg.png', False)
# Inside 20 vs YTG
individual_punter_reg(test, 'YTG', 'in20', 'extra/in20_vs_ytg.png', True)

individual_punter_reg(test, 'YTG', 'downed', 'extra/downed_vs_ytg.png', False)
individual_punter_reg(test, 'YTG', 'FC', 'extra/FC_vs_ytg.png', False)
individual_punter_reg(test, 'YTG', 'touchback', 'extra/touchback_vs_ytg.png', False)
individual_punter_reg(test, 'YTG', 'net', 'extra/net_vs_ytg.png', True)
individual_punter_reg(test, 'YTG', 'gross', 'extra/gross_vs_ytg.png', True)
individual_punter_reg(test, 'touchback', 'norm_net', 'extra/norm-net_vs_touchback.png', False)

    
    


