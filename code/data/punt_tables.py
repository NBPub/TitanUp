# ex for saving HTML, changing to JSON of all HTML strings to load all together
# with open(Path(Path.cwd(),'tables','ex.html'), 'w', encoding='utf-8') as page:
#     page.write(table.style().to_html())



import pandas as pd
import numpy as np
from pathlib import Path
import json

p = Path(Path.cwd(), 'processed data')
    # Load Advanced punting Metrics
adv_cols = ['SHARP_RERUN','ea_punt_epa_above_expected',
               'punter_player_name', 'posteam', 'yardline_100', 'season', 
               'SHARP_RERUN_OF','SHARP_RERUN_PD']
TN_adv = pd.read_parquet(Path(p,'TN_punts_2009-2021_adv.parquet')) # all Titans punts 2009-2021
TN_adv = TN_adv.loc[:,adv_cols]
notTN_adv = pd.read_parquet(Path(p,'notTN_punts_2009-2021_adv.parquet')) # all non-Titans punts 2009-2021
notTN_adv = notTN_adv.loc[:,adv_cols]
punt_adv = pd.read_parquet(Path(p,'punts_2022_adv.parquet')) # all Titans punts 2009-2021
punt_adv = punt_adv.loc[:,adv_cols]
# combine everything
TN_adv = pd.concat([TN_adv, punt_adv])
notTN_adv = pd.concat([notTN_adv,TN_adv[~TN_adv.punter_player_name.isin(['B.Kern','R.Stonehouse'])]])  # all other punts
TN_adv=TN_adv[TN_adv.punter_player_name.isin(['B.Kern','R.Stonehouse'])] # Stonehouse, Kern '09-'21 punts
notTN_adv.loc[:,'punter_player_name'] = 'Rest of NFL'
TN_adv = pd.concat([TN_adv, notTN_adv])


    # Start loading processed punting data
TNpunts = pd.read_parquet(Path(p,'TN_punts_2009-2021.parquet')) # all Titans punts 2009-2021
punts = pd.read_parquet(Path(p, 'punts_2022.parquet')) # all 2022 punts
TNpunts = pd.concat([TNpunts, punts[punts.posteam == 'TEN']]) # Titans punts 2009-2022

# common lists, define at top
percent_rows = ['Touchback','Inside Twenty', 'Fair Catch', 'Out Of Bounds', 'Returned']
comma_rows = ['Punts','Blocked']
epa_rows = ['EPA/play','punt EPA*']
metrics = ['punt_blocked', 'touchback', 'punt_inside_twenty', 'punt_fair_catch', 
           'punt_out_of_bounds','punt_returned','epa']
adv_metrics = {'ea_punt_epa_above_expected':'punt EPA*', 'SHARP_RERUN':'Adj. Net*'}


# Dict for all table strings
punting_tables = {}

    # TN Punters 2009-2022
titans_punters = pd.DataFrame(TNpunts.value_counts(['season','punter_player_name']))
titans_punters.reset_index(inplace=True)
titans_punters.rename(columns={0:'Punts', 'punter_player_name':'Punter'},
          inplace=True)
titans_punters.sort_values('season', inplace=True)

punting_tables['titans_2009-2022'] = titans_punters.style\
        .format_index(lambda v: '')\
        .background_gradient(cmap='Blues', gmap = titans_punters.season)\
        .background_gradient(cmap='Oranges', subset = 'Punts')\
        .set_table_styles([
            {'selector': 'tr:hover','props': [('background-color', '#9c9c2a')]},
            {'selector': 'td', 'props': 'font-size:1.25em;font-weight:bold;'}
                        ])\
        .set_table_attributes('class="table border border-2"').to_html()

    # B.Kern, R.Stonehouse, Rest of NFL
# remove other TN punters
TNpunts=TNpunts[TNpunts.punter_player_name.isin(['B.Kern','R.Stonehouse'])]

# add all other punters as 'Rest of NFL'
p = Path(Path.cwd(), 'processed data', 'notTN_punts_2009-2021.parquet')
others = pd.read_parquet(p)
others = pd.concat([others,TNpunts[~TNpunts.punter_player_name.isin(['B.Kern','R.Stonehouse'])]]) # add other TN punters to others
others = pd.concat([others, punts[punts.posteam != 'TEN']]) # add 2022 data to others
others.loc[:,'punter_player_name'] = 'Rest of NFL'
TNpunts=TNpunts[TNpunts.punter_player_name.isin(['B.Kern','R.Stonehouse'])] # remove other TN punters from Kern/Stonehouse
TNpunts = pd.concat([TNpunts, others])
del others

top_table = pd.DataFrame(columns = TNpunts.punter_player_name.unique())
for val in TNpunts.punter_player_name.unique():
    top_table.loc['Punts',val] = TNpunts[TNpunts.punter_player_name == val].shape[0]
    for col in metrics:
        if col == 'epa':
            top_table.loc['EPA/play',val] = TNpunts[TNpunts.punter_player_name == val][col].mean()
        else:
            top_table.loc[col.replace('punt_','').replace('_',' ').title(),val] = \
                100*TNpunts[TNpunts.punter_player_name == val][col].mean()\
                if col!='punt_blocked' else int(TNpunts[TNpunts.punter_player_name == val][col].sum())
    for met,name in adv_metrics.items():
        top_table.loc[name,val] = TN_adv[TN_adv.punter_player_name == val][met].mean()

punting_tables['top_table'] = top_table.style\
        .format(formatter="{:,}", subset=(comma_rows,top_table.columns))\
        .format(formatter="{:.1f}%", subset=(percent_rows,top_table.columns))\
        .format(formatter="{:.1f}", subset=('Adj. Net*',top_table.columns))\
        .format(formatter="{:.3f}", subset=(epa_rows,top_table.columns))\
        .background_gradient(cmap='bone', vmax=100, subset=(percent_rows,top_table.columns))\
        .background_gradient(cmap='Greens', subset=('EPA/play',top_table.columns), # high=0.5,
                             vmin=top_table.loc['EPA/play',:].min(),vmax=top_table.loc['EPA/play',:].max())\
        .background_gradient(cmap='Greens', subset=('punt EPA*',top_table.columns),
                             vmin=top_table.loc['punt EPA*',:].min(),vmax=top_table.loc['punt EPA*',:].max())\
        .background_gradient(cmap='summer_r', subset=('Adj. Net*',top_table.columns),
                             vmin=top_table.loc['Adj. Net*',:].min(),vmax=top_table.loc['Adj. Net*',:].max())\
        .set_table_styles([
            {'selector': 'td:hover','props': [('background-color', '#0097A6')]},
                       ])\
        .set_table_attributes('class="table table-dark"').to_html()
        
# B.Kern vs Rest of NFL (2017-2019), B.Kern vs Ryan Stonehouse
kern_adv = TN_adv[(TN_adv.season > 2016) & (TN_adv.season < 2020)]
TNpunts = TNpunts[(TNpunts.season > 2016) & (TNpunts.season < 2020)]
kern_table = pd.DataFrame(columns = TNpunts.punter_player_name.unique())
for val in TNpunts.punter_player_name.unique():
    portion = TNpunts[TNpunts.punter_player_name == val]
    kern_table.loc['Punts',val] = portion.shape[0]
    for col in metrics:
        if col == 'epa':
            kern_table.loc['EPA/play',val] = portion[col].mean()
        else:
            kern_table.loc[col.replace('punt_','').replace('_',' ').title(),val] = 100*portion[col].mean()\
            if col!='punt_blocked' else int(portion[col].sum())
    for met,name in adv_metrics.items():
        kern_table.loc[name,val] = kern_adv[kern_adv.punter_player_name == val][met].mean()
kern_stone = kern_table.copy()

punting_tables['kern_table'] = kern_table.style\
        .format(formatter="{:,}", subset=(comma_rows,kern_table.columns))\
        .format(formatter="{:.1f}%", subset=(percent_rows,kern_table.columns))\
        .format(formatter="{:.1f}", subset=('Adj. Net*',kern_table.columns))\
        .format(formatter="{:.3f}", subset=(epa_rows,kern_table.columns))\
        .background_gradient(cmap='bone', vmax=100, subset=(percent_rows,kern_table.columns))\
        .background_gradient(cmap='Greens', subset=('EPA/play',kern_table.columns), #high=0.5,
                             vmin=kern_table.loc['EPA/play',:].min(),vmax=kern_table.loc['EPA/play',:].max())\
        .background_gradient(cmap='Greens', subset=('punt EPA*',kern_table.columns),
                             vmin=kern_table.loc['punt EPA*',:].min(),vmax=kern_table.loc['punt EPA*',:].max())\
        .background_gradient(cmap='summer_r', subset=('Adj. Net*',kern_table.columns),
                             vmin=kern_table.loc['Adj. Net*',:].min(),vmax=kern_table.loc['Adj. Net*',:].max())\
        .set_table_styles([
            {'selector': 'td:hover','props': [('background-color', '#0097A6')]},
                       ])\
        .set_table_attributes('class="table table-dark"').to_html()
del kern_adv

    # R.Stonehouse vs B.Kern ('17-'19)
val = 'R.Stonehouse'
kern_stone.rename(columns = {'B.Kern':"B.Kern '17-'19","Rest of NFL":val}, inplace=True)
portion = punts[punts.punter_player_name==val]
kern_stone.loc['Punts',val] = portion.shape[0]
for col in metrics:
    if col == 'epa':
        kern_stone.loc['EPA/play',val] = portion[col].mean()
    else:
        kern_stone.loc[col.replace('punt_','').replace('_',' ').title(),val] = 100*portion[col].mean()\
        if col!='punt_blocked' else int(portion[col].sum())
for met,name in adv_metrics.items():
    kern_stone.loc[name,val] = TN_adv[TN_adv.punter_player_name == val][met].mean()

punting_tables['kern_stone'] = kern_stone.style\
        .format(formatter="{:,}", subset=(comma_rows,kern_stone.columns))\
        .format(formatter="{:.1f}%", subset=(percent_rows,kern_stone.columns))\
        .format(formatter="{:.1f}", subset=('Adj. Net*',kern_stone.columns))\
        .format(formatter="{:.3f}", subset=(epa_rows,kern_stone.columns))\
        .background_gradient(cmap='bone', vmax=100, subset=(percent_rows,kern_stone.columns))\
        .background_gradient(cmap='Greens', subset=('EPA/play',kern_stone.columns), low=0.5,
                             vmin=kern_stone.loc['EPA/play',:].min(),vmax=kern_stone.loc['EPA/play',:].max())\
        .background_gradient(cmap='Greens', subset=('punt EPA*',kern_stone.columns), low=0.5,
                             vmin=kern_stone.loc['punt EPA*',:].min(),vmax=kern_stone.loc['punt EPA*',:].max())\
        .background_gradient(cmap='summer_r', subset=('Adj. Net*',kern_stone.columns),low=0.5,
                             vmin=kern_stone.loc['Adj. Net*',:].min(),vmax=kern_stone.loc['Adj. Net*',:].max())\
        .set_table_styles([
            {'selector': 'td:hover','props': [('background-color', '#0097A6')]},
                       ])\
        .set_table_attributes('class="table table-dark"').to_html()
del TNpunts, kern_stone, kern_table, top_table, titans_punters

        # Stonehouse vs NFL 2022
analyze = 'R.Stonehouse'
punts.loc[punts[punts.punter_player_name=='R.Stonehouse'].index,'POI'] =analyze
punts.loc[punts[punts.punter_player_name!='R.Stonehouse'].index,'POI'] ='Rest of NFL'
TN_adv = TN_adv[TN_adv.season == 2022]
        
stonehouse = pd.DataFrame(columns = punts.POI.unique())
for val in punts.POI.unique():
    stonehouse.loc['Punts',val] = punts[punts.POI == val].shape[0]
    for col in metrics:
        if col == 'epa':
            stonehouse.loc['EPA/play',val] = punts[punts.POI == val][col].mean()
        else:
            stonehouse.loc[col.replace('punt_','').replace('_',' ').title(),val] = 100*punts[punts.POI == val][col].mean()\
                                                                if col!='punt_blocked' else int(punts[punts.POI == val][col].sum())
    for met,name in adv_metrics.items():
        stonehouse.loc[name,val] = TN_adv[TN_adv.punter_player_name == val][met].mean()

punting_tables['stonehouse2022'] = stonehouse.style\
        .format(formatter="{:,}", subset=(comma_rows,stonehouse.columns))\
        .format(formatter="{:.1f}%", subset=(percent_rows,stonehouse.columns))\
        .format(formatter="{:.1f}", subset=('Adj. Net*',stonehouse.columns))\
        .format(formatter="{:.3f}", subset=(epa_rows,stonehouse.columns))\
        .background_gradient(cmap='bone', vmax=100, subset=(percent_rows,stonehouse.columns))\
        .background_gradient(cmap='Greens', subset=('EPA/play',stonehouse.columns), high=0.5,
                             vmin=stonehouse.loc['EPA/play',:].min(),vmax=stonehouse.loc['EPA/play',:].max())\
        .background_gradient(cmap='Greens', subset=('punt EPA*',stonehouse.columns),
                             vmin=stonehouse.loc['punt EPA*',:].min(),vmax=stonehouse.loc['punt EPA*',:].max())\
        .background_gradient(cmap='summer_r', subset=('Adj. Net*',stonehouse.columns),
                             vmin=stonehouse.loc['Adj. Net*',:].min(),vmax=stonehouse.loc['Adj. Net*',:].max())\
        .set_table_styles([
            {'selector': 'td:hover','props': [('background-color', '#0097A6')]},
            {'selector': 'td, th', 'props': 'font-size:1.1em;'}
                       ])\
        .set_table_attributes('class="table table-dark"').to_html()
del TN_adv
        
# load epa percentiles, team dict, and check columns
p = Path(Path.cwd(), 'processed data', 'percentiles_other_2022.json')
with open(p, 'r') as file:
    measures = json.loads(file.read())    
check = measures.pop('check')
punters = measures.pop('punters')
teams = measures.pop('teams')
measures = {key:np.array(val) for key,val in measures.items()}    
# load team_colors
teamcolors = pd.read_csv(Path(Path.cwd(),'pbp data', 'teamcolors.csv'))
teamcolors.set_index('team',inplace=True,drop=True)
# FIX LA --> LAR
# teamcolors.rename(index = {'LA':'LAR'}, inplace=True)
# teamcolors.drop_duplicates(inplace=True)
teamfix = [punter for punter in teams if teams[punter] =='LA']
for punter in teamfix:
    teams[punter] = 'LAR'

        # Punt Attempts 2022
att_table = pd.DataFrame(punts.value_counts('punter_player_name'))
for val in att_table.index:
    att_table.loc[val,'team'] = teams[val]
att_table.rename(columns={0:'Punts','team':'Team'}, inplace = True)
att_table.rename_axis(index={'punter_player_name':'Punter'}, inplace = True)
att_table.reset_index(inplace=True)

def row_color(v):
    return ['']*2+[f'background-color:{teamcolors.loc[v.Team,"color2"]};color:{teamcolors.loc[v.Team,"color"]}']

punting_tables['punts2022'] = att_table.style\
        .format_index(lambda v: '')\
        .background_gradient(cmap='bone_r', gmap=att_table.Punts)\
        .apply(row_color, axis=1)\
        .set_table_styles([
            {'selector': 'td:hover','props': [('background-color', '#0097A6')]},
            {'selector': 'td, th', 'props': 'font-weight:bold;'},
            {'selector': 'th', 'props': [('position','sticky'),('top',0)]},
                       ])\
        .set_table_attributes('class="table table-dark"').to_html()

    # Punt Normalized Net Yards, Return Rate 2022
test = pd.DataFrame(columns=['Team','Name','Norm.Net','Norm.Gross','Return%', 'Punts'])
k=1
for val in punters.keys():
    sub = punts[punts.punter_player_name == val]
    if sub.shape[0] >= 30: # 30 PUNT MINIMUM FOR PUNTER FOR SEASON
        test.loc[k,'Name'] = val
        test.loc[k,'Team'] = teams[val]   
        test.loc[k,'Norm.Net'] = np.mean(sub.net_yards/sub.yardline_100)
        test.loc[k,'Norm.Gross'] = np.mean(sub.kick_distance/sub.yardline_100)
        test.loc[k,'Return%'] = sub.punt_returned.mean()
        test.loc[k,'Punts'] = int(sub.shape[0])
        k+=1
test.Punts = test.Punts.astype('int')
test['Return%'] = test['Return%'].astype('float')
test['Norm.Net'] = test['Norm.Net'].astype('float')
test['Norm.Gross'] = test['Norm.Gross'].astype('float')
test.sort_values('Norm.Net', ascending=False,inplace=True)
test['Return%'] = 100*test['Return%']

def row_color(v):
    return [f'background-color:{teamcolors.loc[v.Team,"color"]};color:{teamcolors.loc[v.Team,"color2"]}']+['']*4

test2 = test.drop(columns = 'Norm.Gross')
punting_tables['normnet2022'] = test2.style\
        .format_index(lambda v: '')\
        .format(formatter="{:.0f}%", subset='Return%')\
        .format(formatter="{:.3f}", subset='Norm.Net')\
        .background_gradient(cmap='PiYG', subset='Norm.Net', )\
        .background_gradient(cmap='PiYG', subset='Return%')\
        .background_gradient(cmap='bone_r', subset='Punts')\
        .apply(row_color, axis=1)\
        .set_table_styles([
            {'selector': 'td:hover','props': [('background-color', '#0097A6')]},
            {'selector': 'th', 'props': [('position','sticky'),('top',0)]},
                       ])\
        .set_table_attributes('class="table table-dark"').to_html()

test2 = test.drop(columns = 'Norm.Net')
test2.sort_values('Norm.Gross', ascending=False,inplace=True)
punting_tables['normgross2022'] = test2.style\
        .format_index(lambda v: '')\
        .format(formatter="{:.0f}%", subset='Return%')\
        .format(formatter="{:.3f}", subset='Norm.Gross')\
        .background_gradient(cmap='PiYG', subset='Norm.Gross', )\
        .background_gradient(cmap='PiYG', subset='Return%')\
        .background_gradient(cmap='bone_r', subset='Punts')\
        .apply(row_color, axis=1)\
        .set_table_styles([
            {'selector': 'td:hover','props': [('background-color', '#0097A6')]},
            {'selector': 'th', 'props': [('position','sticky'),('top',0)]},
                       ])\
        .set_table_attributes('class="table table-dark"').to_html()
del test, att_table, stonehouse, test2

    # Punter Advanced Metrics, 2022
p = Path(Path.cwd(), 'processed data', 'punts_2022_adv.parquet')
punts = pd.read_parquet(p)

test = pd.DataFrame()
k=1
for val in punters.keys():
    sub = punts[punts.punter_player_name == val]
    if sub.shape[0] >= 30: # 30 PUNT MINIMUM FOR PUNTER FOR SEASON
        test.loc[k,'Team'] = teams[val]
        test.loc[k,'Name'] = val
        test.loc[k,'Punt EPA*'] = sub.ea_punt_epa_above_expected.mean()
        test.loc[k,'Adj. Net*'] = sub.SHARP_RERUN.mean()
        test.loc[k,'Punts'] = int(sub.shape[0])
        test.loc[k,'Open Field'] = sub.SHARP_RERUN_PD.mean()
        test.loc[k,'Pin Deep'] = sub.SHARP_RERUN_OF.mean()
        k+=1
test.Punts = test.Punts.astype('int')
test.sort_values('Punt EPA*', ascending=False,inplace=True)   

def row_color(v):
    return [f'background-color:{teamcolors.loc[v.Team,"color2"]};color:{teamcolors.loc[v.Team,"color"]}']+['']*6

punting_tables['adv2022'] = test.style\
        .format_index(lambda v: '')\
        .format(formatter="{:.1f}", subset=['Adj. Net*', 'Pin Deep','Open Field'])\
        .format(formatter="{:.3f}", subset='Punt EPA*')\
        .background_gradient(cmap='PiYG', subset='Adj. Net*', )\
        .background_gradient(cmap='PiYG', subset='Punt EPA*')\
        .background_gradient(cmap='bone_r', subset='Punts')\
        .background_gradient(cmap='coolwarm_r', subset='Pin Deep')\
        .background_gradient(cmap='coolwarm_r', subset='Open Field')\
        .apply(row_color, axis=1)\
        .set_table_styles([
            {'selector': 'td:hover','props': [('background-color', '#0097A6')]},
            {'selector': 'td','props': [('padding', '0.5em 1em')]},
            {'selector': 'th', 'props': [('position','sticky'),('top',0)]},
                       ])\
        .set_table_attributes('class="table table-dark"').to_html() 
del test    
    

    # Punters are Players! 2022
# load processed data
p = Path(Path.cwd(), 'processed data', 'punts_other_2022.parquet')
punts = pd.read_parquet(p)

# Gather Passing,Rushing,Receiving,Tackling into separate tables. 
# Save play descriptions as dictionary
p_also = {
    'passing':{},
    'rushing':{},
    'receiving':{},
    'tackling':{},
}
ppass = pd.DataFrame()
prush = pd.DataFrame()
prec = pd.DataFrame()
ptack = pd.DataFrame(index = punters.keys(), columns = ['Solo','Asst','for Loss'])
ptack.loc[:,:] = 0

for val in check:
    if val.startswith('passer_'):
        sub = punts[punts.passer_player_id.notnull()]
        for name in sub.passer_player_name:
            sub2 = sub[sub.passer_player_name == name]
            ppass.loc[name,'Attempts'] = sub2.shape[0]
            ppass.loc[name,'Y/A'] = sub2.passing_yards.sum()/sub2.shape[0]
            ppass.loc[name,'Comp %'] = "{:.0%}".format(sub2.complete_pass.mean())
            ppass.loc[name,'TD'] = sub2.pass_touchdown.sum()
            ppass.loc[name,'Int'] = sub2.interception.sum()
            ppass.loc[name,'EPA/play'] = sub2.qb_epa.mean()
            ppass.loc[name,'EPA percentile'] = np.searchsorted(measures["pass_epa"],sub2.qb_epa.mean())
            
            p_also['passing'][name] = '<br>'.join([f'Week {sub2.loc[val,"week"]} - {sub2.loc[val,"home_team"]} at {sub2.loc[val,"away_team"]}: {sub2.loc[val,"desc"]}'\
                                                   for val in sub2.index])

    elif val.startswith('rusher_'):
        sub = punts[punts.rusher_id.notnull()]
        for name in sub.rusher_player_name:
            sub2 = sub[sub.rusher_player_name == name]
            prush.loc[name,'Attempts'] = sub2.shape[0]
            prush.loc[name,'Y/A'] = sub2.rushing_yards.sum()/sub2.shape[0]
            prush.loc[name,'First Down %'] = "{:.0%}".format(sub2.first_down_rush.mean())
            prush.loc[name,'TD'] = sum(sub2.td_player_name == name)
            prush.loc[name,'Fumbles'] = sum(sub2.fumbled_1_player_name == name) + sum(sub2.fumbled_2_player_name == name)          
            prush.loc[name,'EPA/play'] = sub2.epa.mean()
            prush.loc[name,'EPA percentile'] = np.searchsorted(measures["rush_epa"],sub2.epa.mean())
            p_also['rushing'][name] = '<br>'.join([f'Week {sub2.loc[val,"week"]} - {sub2.loc[val,"home_team"]} at {sub2.loc[val,"away_team"]}: {sub2.loc[val,"desc"]}'\
                                                   for val in sub2.index])
    elif val.startswith('receiver_player_id'):
        sub = punts[punts.receiver_player_id.notnull()]
        for name in sub.receiver_player_name:
            sub2 = sub[sub.receiver_player_name == name]
            prec.loc[name,'Targets'] = sub2.shape[0]
            prec.loc[name,'Catches'] = sub2.receiving_yards.notnull().sum()
            prec.loc[name,'Y/T'] = sub2.receiving_yards.sum()/sub2.shape[0]
            prec.loc[name,'TD'] = sum(sub2.td_player_name == name)
            prec.loc[name,'YAC EPA oe'] = np.mean(sub2.yac_epa-sub2.xyac_epa)          
            prec.loc[name,'EPA/play'] = sub2.epa.mean()
            prec.loc[name,'EPA percentile'] = np.searchsorted(measures["rec_epa"],sub2.epa.mean())
            p_also['receiving'][name] = '<br>'.join([f'Week {sub2.loc[val,"week"]} - {sub2.loc[val,"home_team"]} at {sub2.loc[val,"away_team"]}: {sub2.loc[val,"desc"]}'\
                                                   for val in sub2.index])
    else: # TACKLES
        sub = punts[punts[val].notnull()]
        for name in punters.keys():
            if val.startswith('solo_tackle'):
                ptack.loc[name, 'Solo'] += sum(sub[val.replace('_id','_name')] == name)
            elif val.startswith('tackle_for_loss'):
                ptack.loc[name, 'for Loss'] += sum(sub[val.replace('_id','_name')] == name)
            else:
                ptack.loc[name, 'Asst'] += sum(sub[val.replace('_id','_name')] == name)
            
            if name in p_also['tackling'].keys():
                p_also['tackling'][name] = '<br>'.join([p_also['tackling'][name],'<br>'.join([f'Week {sub.loc[val,"week"]} - {sub.loc[val,"home_team"]} at {sub.loc[val,"away_team"]}: {sub.loc[val,"desc"]}'\
                                       for val in sub[sub[val.replace('_id','_name')] == name].index])])           
            else:
                p_also['tackling'][name] = '<br>'.join([f'Week {sub.loc[val,"week"]} - {sub.loc[val,"home_team"]} at {sub.loc[val,"away_team"]}: {sub.loc[val,"desc"]}'\
                                       for val in sub[sub[val.replace('_id','_name')] == name].index])
                
ppass = ppass.convert_dtypes() if not ppass.empty else None
prush = prush.convert_dtypes() if not prush.empty  else None
prec = prec.convert_dtypes() if not prec.empty else None  
ptack.replace(0,np.nan, inplace = True)
ptack.dropna(how='all', inplace = True)
ptack = ptack if not ptack.empty else None 

tackle_fix = {}
for key,val in p_also['tackling'].items():
    if val != '<br><br><br>':
        tackle_fix[key] = val.replace('<br><br><br>','').replace('<br><br>','')
p_also['tackling'] = tackle_fix


# Save play descriptions to JSON file
with open(Path(Path.cwd(),'processed data','punter_other_desc_2022.json'), 'w', encoding='utf-8') as file:
    file.write(json.dumps(p_also))


# Convert non-empty data into styled HTML, save
classes = 'class="table table-dark"'
styles = [{'selector': 'td:hover','props': [('background-color', '#0097A6')]}]

punting_tables['2022_passing'] = ppass.style\
    .format(formatter={'Y/A': "{:.1f}", 'EPA/play': "{:.2f}"})\
    .format_index(lambda v: f'{v} {teams[v]}')\
    .background_gradient(axis=0,subset='EPA percentile', cmap='PiYG', vmin=0, vmax=100)\
    .set_table_styles(styles)\
    .set_table_attributes(classes).to_html() if isinstance(ppass,pd.DataFrame) else None

punting_tables['2022_rushing'] = prush.style\
    .format(formatter={'Y/A': "{:.1f}", 'EPA/play': "{:.2f}"})\
    .format_index(lambda v: f'{v} {teams[v]}')\
    .background_gradient(axis=0,subset='EPA percentile', cmap='PiYG', vmin=0, vmax=100)\
    .set_table_styles([{'selector': 'td:hover','props': [('background-color', '#0097A6')]}])\
    .set_table_attributes('class="table table-dark"').to_html() if isinstance(prush,pd.DataFrame) else None

punting_tables['2022_receiving'] = prec.style\
    .format(formatter={'Y/T': "{:.1f}", 'EPA/play': "{:.2f}", 'YAC EPA oe': "{:.2f}"})\
    .format_index(lambda v: f'{v} {teams[v]}')\
    .background_gradient(axis=0,subset='EPA percentile', cmap='PiYG', vmin=0, vmax=100)\
    .set_table_styles(styles)\
    .set_table_attributes(classes).to_html() if isinstance(prec,pd.DataFrame) else None

punting_tables['2022_tackling'] = ptack.style\
    .format(precision=0, na_rep='')\
    .format_index(lambda v: f'{v} {teams[v]}')\
    .background_gradient(axis=0, cmap='ocean', vmin=0, vmax=ptack.max().values[0])\
    .set_table_styles([
            {'selector': 'td:hover','props': [('background-color', '#0097A6')]},
            {'selector': 'td', 'props': 'font-size:16;font-weight:bold;'}
                    ])\
    .set_table_attributes(classes).to_html() if isinstance(ptack,pd.DataFrame) else None
          
        # Punters are Players! Titans
# load processed data, player names, and check columns
p = Path(Path.cwd(), 'processed data', 'TN_other-KernStone.parquet')
punts = pd.read_parquet(p)
p = Path(Path.cwd(), 'processed data', 'TN_other-KernStone.json')
with open(p, 'r') as file:
    punters = json.loads(file.read())    
check = punters.pop('check columns')

# Gather Passing,Rushing,Receiving,Tackling into separate tables. 
# Save play descriptions as dictionary
p_also = {
    'passing':{},
    'rushing':{},
    'receiving':{},
    'tackling':{},
}
ppass = pd.DataFrame()
prush = pd.DataFrame()
prec = pd.DataFrame()
ptack = pd.DataFrame(index = punters.keys(), columns = ['Solo','Asst','for Loss'])
ptack.loc[:,:] = 0

for val in check:
    if val.startswith('passer_'):
        sub = punts[punts.passer_player_id.notnull()]
        for name in sub.passer_player_name:
            sub2 = sub[sub.passer_player_name == name]
            ppass.loc[name,'Attempts'] = sub2.shape[0]
            ppass.loc[name,'Y/A'] = sub2.passing_yards.sum()/sub2.shape[0]
            ppass.loc[name,'Comp %'] = "{:.0%}".format(sub2.complete_pass.mean())
            ppass.loc[name,'TD'] = sub2.pass_touchdown.sum()
            ppass.loc[name,'Int'] = sub2.interception.sum()
            ppass.loc[name,'EPA/play'] = sub2.qb_epa.mean()
            ppass.loc[name,'EPA percentile'] = np.searchsorted(measures["pass_epa"],sub2.qb_epa.mean())
            
            p_also['passing'][name] = '<br>'.join([f'{sub.loc[val,"season"]} Week {sub2.loc[val,"week"]} - {sub2.loc[val,"home_team"]} at {sub2.loc[val,"away_team"]}: {sub2.loc[val,"desc"]}'\
                                                   for val in sub2.index])

    elif val.startswith('rusher_'):
        sub = punts[punts.rusher_id.notnull()]
        for name in sub.rusher_player_name:
            sub2 = sub[sub.rusher_player_name == name]
            prush.loc[name,'Attempts'] = sub2.shape[0]
            prush.loc[name,'Y/A'] = sub2.rushing_yards.sum()/sub2.shape[0]
            prush.loc[name,'First Down %'] = "{:.0%}".format(sub2.first_down_rush.mean())
            prush.loc[name,'TD'] = sum(sub2.td_player_name == name)
            prush.loc[name,'Fumbles'] = sum(sub2.fumbled_1_player_name == name) + sum(sub2.fumbled_2_player_name == name)          
            prush.loc[name,'EPA/play'] = sub2.epa.mean()
            prush.loc[name,'EPA percentile'] = np.searchsorted(measures["rush_epa"],sub2.epa.mean())
            p_also['rushing'][name] = '<br>'.join([f'{sub.loc[val,"season"]} Week {sub2.loc[val,"week"]} - {sub2.loc[val,"home_team"]} at {sub2.loc[val,"away_team"]}: {sub2.loc[val,"desc"]}'\
                                                   for val in sub2.index])
    elif val.startswith('receiver_player_id'):
        sub = punts[punts.receiver_player_id.notnull()]
        for name in sub.receiver_player_name:
            sub2 = sub[sub.receiver_player_name == name]
            prec.loc[name,'Targets'] = sub2.shape[0]
            prec.loc[name,'Catches'] = sub2.receiving_yards.notnull().sum()
            prec.loc[name,'Y/T'] = sub2.receiving_yards.sum()/sub2.shape[0]
            prec.loc[name,'TD'] = sum(sub2.td_player_name == name)
            prec.loc[name,'YAC EPA oe'] = np.mean(sub2.yac_epa-sub2.xyac_epa)          
            prec.loc[name,'EPA/play'] = sub2.epa.mean()
            prec.loc[name,'EPA percentile'] = np.searchsorted(measures["rec_epa"],sub2.epa.mean())
            p_also['receiving'][name] = '<br>'.join([f'{sub.loc[val,"season"]} Week {sub2.loc[val,"week"]} - {sub2.loc[val,"home_team"]} at {sub2.loc[val,"away_team"]}: {sub2.loc[val,"desc"]}'\
                                                   for val in sub2.index])
    else: # TACKLES
        sub = punts[punts[val].notnull()]
        for name in punters.keys():
            if val.startswith('solo_tackle'):
                ptack.loc[name, 'Solo'] += sum(sub[val.replace('_id','_name')] == name)
            elif val.startswith('tackle_for_loss'):
                ptack.loc[name, 'for Loss'] += sum(sub[val.replace('_id','_name')] == name)
            else:
                ptack.loc[name, 'Asst'] += sum(sub[val.replace('_id','_name')] == name)
            
            if name in p_also['tackling'].keys():
                p_also['tackling'][name] = '<br>'.join([p_also['tackling'][name],'<br>'.join([f'{sub.loc[val,"season"]} Week {sub.loc[val,"week"]} - {sub.loc[val,"home_team"]} at {sub.loc[val,"away_team"]}: {sub.loc[val,"desc"]}'\
                                       for val in sub[sub[val.replace('_id','_name')] == name].index])])           
            else:
                p_also['tackling'][name] = '<br>'.join([f'{sub.loc[val,"season"]} Week {sub.loc[val,"week"]} - {sub.loc[val,"home_team"]} at {sub.loc[val,"away_team"]}: {sub.loc[val,"desc"]}'\
                                       for val in sub[sub[val.replace('_id','_name')] == name].index])
                
ppass = ppass.convert_dtypes() if not ppass.empty else None
prush = prush.convert_dtypes() if not prush.empty  else None
prec = prec.convert_dtypes() if not prec.empty else None  
ptack.replace(0,np.nan, inplace = True)
ptack.dropna(how='all', inplace = True)
ptack = ptack if not ptack.empty else None 



tackle_fix = {}
for key,val in p_also['tackling'].items():
    if val!='':
        if val != '<br><br><br>':
            tackle_fix[key] = val.replace('<br><br><br>','').replace('<br><br>','')
p_also['tackling'] = tackle_fix

# Save play descriptions to JSON file
with open(Path(Path.cwd(),'processed data','punter_other_desc_Titans.json'), 'w', encoding='utf-8') as file:
    file.write(json.dumps(p_also))

# Convert non-empty data into styled HTML, save
punting_tables['PuntTit_passing'] = ppass.style\
    .format(formatter={'Y/A': "{:.1f}", 'EPA/play': "{:.2f}"})\
    .background_gradient(axis=0,subset='EPA percentile', cmap='PiYG', vmin=0, vmax=100)\
    .set_table_styles(styles)\
    .set_table_attributes(classes).to_html() if isinstance(ppass,pd.DataFrame) else None

punting_tables['PuntTit_rushing'] = prush.style\
    .format(formatter={'Y/A': "{:.1f}", 'EPA/play': "{:.2f}"})\
    .background_gradient(axis=0,subset='EPA percentile', cmap='PiYG', vmin=0, vmax=100)\
    .set_table_styles([{'selector': 'td:hover','props': [('background-color', '#0097A6')]}])\
    .set_table_attributes('class="table table-dark"').to_html() if isinstance(prush,pd.DataFrame) else None

punting_tables['PuntTit_receiving'] = prec.style\
    .format(formatter={'Y/T': "{:.1f}", 'EPA/play': "{:.2f}", 'YAC EPA oe': "{:.2f}"})\
    .background_gradient(axis=0,subset='EPA percentile', cmap='PiYG', vmin=0, vmax=100)\
    .set_table_styles(styles)\
    .set_table_attributes(classes).to_html() if isinstance(prec,pd.DataFrame) else None

punting_tables['PuntTit_tackling'] = ptack.style\
    .format(precision=0, na_rep='')\
    .background_gradient(axis=0, cmap='ocean', vmin=0, vmax=ptack.max().values[0])\
    .set_table_styles([
            {'selector': 'td:hover','props': [('background-color', '#0097A6')]},
            {'selector': 'td', 'props': 'font-size:16;font-weight:bold;'}
                    ])\
    .set_table_attributes(classes).to_html() if isinstance(ptack,pd.DataFrame) else None


# Final Save - JSON with HTML table strings
p = Path(Path.cwd(), 'tables', 'punting_tables.json')
with open(p, 'w', encoding='utf-8') as file:
    file.write(json.dumps(punting_tables)) 
    
del punts, p_also, punting_tables, ptack, prec, prush, ppass, measures