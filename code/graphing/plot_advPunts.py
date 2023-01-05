import pandas as pd
import numpy as np
from pathlib import Path
import json

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects 

    # Intro
# punt EPA vs Yds to Go, par graph
def epa_bar(punts):   
    plt.figure(figsize=(4,3), facecolor='gainsboro')
    ax = sns.barplot(data=punts, x='yardline_100', y='ea_punt_epa_above_expected', width=4, errwidth=0.5, color='k', errcolor='magenta', alpha=0.6)
    bounds = ax.get_xbound()    
    ax.set_xlim(bounds[0]+12,bounds[1])
    bounds = ax.get_xbound()     
    ax.set_xticks(np.arange(bounds[0]+0.5, bounds[1]-0.5, 5, dtype='int'))
    ax.set_ylim(-.15,.15)
    offset = bounds[1]-100
    
    # dumb way to fill colors, get means for each bin then collapse
    x = {}
    for val in np.arange(40,100,4):
        x[val] = 'green' if punts[(punts.yardline_100>=val)&(punts.yardline_100<(val+4))].epa.mean() > 0 else 'red'
    start = list(x.keys())[0]
    y = {start:x.pop(start)}
    current = y[start]
    for key,val in x.items():
        if val != current:
            y[key] = val
            current = val
    y[100] = current
    keys = list(y.keys())
    for i,val in enumerate(keys):
        if val == 100:
            break
        if y[val] == 'red':
            ax.fill_between((val+offset,keys[i+1]+offset),-0.15,0, color='red',alpha=0.15)
        else:
            ax.fill_between((val+offset,keys[i+1]+offset),0,0.15, color='seagreen',alpha=0.15)
    ax.set_title('Punt EPA* vs Yds to go', y=0.9, loc='center', fontweight='bold')
    ax.set_ylabel('Punt EPA*', fontweight='bold',fontsize='large')
    ax.set_xlabel('Yards to go', labelpad=1)
    
    plt.savefig('graphs/Intro/bar_pEPA.png',dpi=300,bbox_inches='tight')
    #plt.show()
    plt.close()
    
def historical_SHARP(punts):
    test = pd.DataFrame()
    k = 1
    for val in punts.punter_player_name.unique():
        sub = punts[punts.punter_player_name == val]
        for year in sub.season.unique():
            sub2 = sub[sub.season == year]
            if sub2.shape[0] > 30: # 30 PUNT MINIMUM FOR PUNTER FOR SEASON
                test.loc[k,'name'] = val
                test.loc[k,'season'] = year
                test.loc[k,'punts'] = int(sub2.shape[0])
                test.loc[k,'return_rate'] = sub2.returned.mean()
                test.loc[k,'SHARP'] = sub2.SHARP_RERUN.mean()
                k+=1
    for val in ['season','punts']:
        test[val] = test[val].astype('int')
    
    metric = 'SHARP'
    against = 'return_rate'
    
    kern = test[test.name == 'B.Kern'].sort_values(metric,ascending=False)[0:6]
    kern2 = test[test.name == 'B.Kern'].sort_values(metric,ascending=False)[6:]            
    settings = {'figure.figsize':[10, 8], 'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
      'axes.labelweight':'bold','axes.labelsize':'x-large',
      'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 'savefig.dpi': 300, 'savefig.bbox':'tight'}   
    
    stone = test[test.name == 'R.Stonehouse']
    top_3 = test.sort_values(metric, ascending=False)[0:5]
    top_3.reset_index(drop=True,inplace=True)
    if not top_3[top_3.name == 'R.Stonehouse'].empty:
        ind = top_3[top_3.name == 'R.Stonehouse'].index[0]
        ind = f'{ind+1}. '
        top_3 = top_3[top_3.name != 'R.Stonehouse']
    else:
        ind = ''
    
    with plt.rc_context(settings):
        ax = sns.regplot(data=test,x=against,y=metric, scatter_kws={'alpha':0.5}, color='grey') # all data
        sns.regplot(data=test[test.name == 'B.Kern'],x=against,y=metric, scatter_kws={'alpha':0.75}, color='magenta') # Kern data
        ax.plot(stone[against],stone[metric],'o', color='orange') # Stone data
        bounds = (ax.get_xlim(), ax.get_ylim())
    
        ax.plot((test[against].mean(),test[against].mean()),bounds[1],'--',color='grey',lw=0.5)
        ax.plot(bounds[0],(test[metric].mean(),test[metric].mean()),'--',color='grey',lw=0.5)
    
        ax.set_xlim(bounds[0])
        ax.set_ylim(bounds[1])
        x_pos = np.linspace(bounds[0][0],bounds[0][1], 20)
        y_pos = np.linspace(bounds[1][0],bounds[1][1], 20)
    
        plt.annotate(f"{ind}{stone['name'][stone.index[0]]}", (stone[against],stone[metric]), 
                     ha='center',va='bottom', color='darkorange', fontweight='bold', fontsize='large')
        
        plt.text(x_pos[4],y_pos[15],'B.Kern', color='magenta',fontsize='large')
        
        for val in kern.index:
            plt.annotate(f"'{str(kern.season[val])[-2:]}", (kern[against][val],kern[metric][val]+.1), 
                         ha='right',va='bottom', color='magenta', fontweight='bold')
        for val in kern2.index:
            plt.annotate(f"'{str(kern2.season[val])[-2:]}", (kern2[against][val],kern2[metric][val]), 
                         ha='left',va='top', color='magenta', fontweight='bold')    
    
        plt.text(x_pos[1],y_pos[3],f"NFL('09-'22)\n{test.shape[0]} punter seasons", color='grey',fontsize='large')
    
        va = 'bottom'
        for val in top_3.index:
            va = 'bottom' if va == 'top' else 'top'
            correct = -1 if va == 'top' else 1
            ax.plot(top_3[against][val],top_3[metric][val],'o', color='green')
            plt.annotate(f"{val+1}. {top_3.name[val]} '{str(top_3.season[val])[-2:]}", 
                         (top_3[against][val]+.003,top_3[metric][val]+correct*.1), 
                         ha='left',va=va, color='green', fontweight='bold')
    
    
        plt.xlabel('Return Rate')
        plt.ylabel('Adj Net*')
             
        plt.savefig('graphs/kern v stonehouse/historical-SHARP-v-returnrate.png')
    # plt.show()
    plt.close()

def kern_history_bar(punts): # SHARP RERUN, pEPA vs NFL, `09-`21
    kern = pd.DataFrame()    
    for year in punts.season.unique():
        d = punts[punts.season == year]
        kern.loc[year,'pEPA'] = d[d.punter_player_name=='B.Kern'].ea_punt_epa_above_expected.mean() \
                               -d[d.punter_player_name!='B.Kern'].ea_punt_epa_above_expected.mean()
        
        kern.loc[year,'Net'] = d[d.punter_player_name=='B.Kern'].SHARP_RERUN.mean() \
                              -d[d.punter_player_name!='B.Kern'].SHARP_RERUN.mean()    
    
    
    settings = {'figure.figsize':[6, 8],'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',
  'axes.labelweight':'bold', 'axes.labelsize':'x-large', 'axes.formatter.limits':(0,2),
  'xtick.color':'k', 'font.weight':'bold', 'savefig.dpi': 300, 'savefig.bbox':'tight'}  
    with plt.rc_context(settings):    
        for i,metric in enumerate(['Net','pEPA']):
            plt.subplot(2,1,i+1)
            
            colors = ['magenta' if val else 'lime' for val in kern[metric] > 0]
            plt.bar(x=kern.index, height = kern[metric], color=colors)
            plt.xticks(ticks = kern.index, labels = [f"'{str(val)[-2:]}" for val in kern.index])
            
            if metric == 'Net':
                plt.ylabel('Adj. Net*')
            else:
                plt.ylabel('Punt EPA*')
            plt.title('  Kern - NFL, yearly avg', y=0.9, loc='left', 
                      fontweight='bold', color='darkblue')
    
    
        plt.savefig('graphs/kern history/adv_bar.png')
        # plt.show()
    plt.close()

def kern_history_pEPA_reg(punts): # pEPA vs Yds to go regression vs Year, Blue/Orange scheme
    settings = {'figure.figsize':[12, 8],'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
      'axes.grid':True, 'grid.color':'dimgrey','axes.grid.axis':'both','axes.labelweight':'bold',
      'grid.alpha':0.5, 'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 
      'savefig.dpi': 300, 'savefig.bbox':'tight', 'axes.formatter.limits':(0,2)}          
    
    with plt.rc_context(settings):
        g = sns.lmplot(data = punts, x = 'yardline_100', y = 'ea_punt_epa_above_expected',
                       hue='punter_player_name',hue_order=['Rest of NFL', 'B.Kern'],
                       scatter=False, legend=False,  row='season', order=2,
                       line_kws={'lw':5, 'scaley':True,'label':['Kern','NFL']},
                       facet_kws={'legend_out':False,'sharex':False,})

        g.set_ylabels('Punt EPA*')
    
        for ax in g.axes.ravel():
            ax.legend(labelcolor=['royalblue','darkorange'], frameon=False, loc='upper center')
            ax.set_xlabel('Yards to go')           
        g.set_titles(template='{row_name}', y=0.3, fontweight='heavy', fontsize=54)
    
        plt.savefig('graphs/kern history/PuntEPA_Reg_adv.png')
        # plt.show()
        plt.close()

def kern_stone_pEPA_reg(punts, metric): # pEPA vs Yds to go regression, Blue/Green scheme
    settings = {'figure.figsize':[12, 8],'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
      'axes.grid':True, 'grid.color':'dimgrey','axes.grid.axis':'both','axes.labelweight':'bold',
      'grid.alpha':0.5, 'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 
      'savefig.dpi': 300, 'savefig.bbox':'tight', 'axes.formatter.limits':(0,3)} 
        
    with plt.rc_context(settings):
        g = sns.lmplot(data = punts, x = 'yardline_100', y = metric, order=2,
                       hue='punter_player_name', scatter=False, legend=False, palette='Accent_r',
                       line_kws={'lw':4},facet_kws={'legend_out':False, 'sharex':False})
        g.set_xlabels('Yards to go')
        if metric == 'ea_punt_epa_above_expected':
            g.set_ylabels('Punt EPA*')
            savename = 'LM-puntEPA_adv'
        else:
            g.set_ylabels('Adj. Net*')
            savename = 'LM-SHARP-RERUN_adv'
    
        for ax in g.axes.ravel():
            ax.legend(labelcolor=['deeppink','orange'], frameon=False, loc='upper left')
            ax.set_xlabel('Yards to go')    
        plt.tick_params(axis='y',labelleft=True, pad=0)
        
        plt.savefig(f'graphs/kern v stonehouse/{savename}.png')
        # plt.show()
        plt.close()  

def stone_nfl_pEPA_reg(punts): # pEPA vs Yds to go regression, Blue/Orange scheme
    punts.loc[punts[punts.punter_player_name != 'R.Stonehouse'].index,'punter_player_name'] = 'Rest of NFL'
    settings = {'figure.figsize':[12, 8],'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
      'axes.grid':True, 'grid.color':'dimgrey','axes.grid.axis':'both','axes.labelweight':'bold',
      'grid.alpha':0.5, 'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 
      'savefig.dpi': 300, 'savefig.bbox':'tight', 'axes.formatter.limits':(0,2)}              
    with plt.rc_context(settings):
        g = sns.lmplot(data = punts, x = 'yardline_100', y = 'ea_punt_epa_above_expected',
                       hue='punter_player_name',
                       scatter=False, legend=False, order=2,
                       line_kws={'lw':5, 'scaley':True,'label':['Stonehouse','NFL']},
                       facet_kws={'legend_out':False,'sharex':False,})

        g.set_ylabels('Punt EPA*')
    
        for ax in g.axes.ravel():
            ax.legend(labelcolor=['royalblue','darkorange'], frameon=False, loc='upper center')
            ax.set_xlabel('Yards to go')           
    
        plt.savefig('graphs/stonehouse/PuntEPA_Reg_adv.png')
        # plt.show()
        plt.close()

def individual_punter_adv(data, col1, col2, savename, xlabel, ylabel): # individual plots, see Stone
    settings = {'figure.figsize':[8, 8], 'figure.facecolor':'#232323', 'figure.edgecolor':'w',  \
  'axes.labelcolor':'w','axes.edgecolor':'w', 'xtick.color':'w','ytick.color':'w',
  'axes.labelweight':'bold','axes.labelsize':'x-large','ytick.labelsize':'large', 'xtick.labelsize':'large',
  'font.weight':'bold', 'savefig.dpi': 300, 'savefig.bbox':'tight'}   
   
    check_factor = 0.25   
    with plt.rc_context(settings):
        # Regression line and Scatter
        sns.regplot(data=data,x=col1,y=col2, scatter=False, color='k',line_kws={'alpha':0.3}, order=1)
        plt.scatter(x=data[col1],y=data[col2], s=data['punts']*3, c=data['color'], edgecolors=data['c2'])
        bounds = plt.axis()
        
        # Mean lines
        plt.plot((data[col1].mean(),data[col1].mean()),bounds[2:],'--',color='grey',lw=0.5) 
        plt.plot(bounds[0:2],(data[col2].mean(),data[col2].mean()),'--',color='grey',lw=0.5)
        plt.axis(bounds)
    
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        
        x_check = 1.5*check_factor*(bounds[1]-bounds[0])
        y_check = check_factor*(bounds[3]-bounds[2])
        y_txt = y_check/25
        
        # Punter labels
        named = pd.DataFrame(columns = data.columns)
        for val in data.index:
            check = abs(data.loc[val,[col1,col2]] - named.loc[:,[col1,col2]])
            check = check[(check[col1]<x_check) & (check[col2]<y_check)] #
            if check.shape[0] % 2 == 1:
                plt.annotate(data.name[val], (data.loc[val,col1], data.loc[val,col2]-y_txt),
                            fontsize='small', ha='left', va='top', color=data.loc[val,'color'],
                            path_effects=[path_effects.Stroke(linewidth=1.2, foreground=data.loc[val,'c2']),path_effects.Normal()]
                            )                                    
                                          
            else:
                plt.annotate(data.name[val], (data.loc[val,col1], data.loc[val,col2]+y_txt),
                            fontsize='small', ha='right', va='bottom', color=data.loc[val,'color'],
                            path_effects=[path_effects.Stroke(linewidth=1.2, foreground=data.loc[val,'c2']),path_effects.Normal()]
                            )         
    
            named.loc[val,:] = data.loc[val,:]
        plt.savefig(f'graphs/stonehouse/individuals_adv/{savename}.png')
    # plt.show()
    plt.close()


    # Load Data, send to graphs
p = Path(Path.cwd(),'pbp data')
data = pd.read_csv(Path(p,'puntalytics.csv')) # Puntalytics data from 1999-2022
data = data[data.season.isin(range(2009,2023))] # select from 2009-present

    ## All Data - pEPA bar chart, historical SHARP vs Return Rate
epa_bar(data)
historical_SHARP(data)
    

    ## Kern History - pEPA/Sharp bar, pEPA regressions
sub = data[data.season.isin(range(2009,2022))]
sub.loc[sub[sub.punter_player_name != 'B.Kern'].index,'punter_player_name'] = 'Rest of NFL'
kern_history_bar(sub)
sub = sub[sub.season.isin(range(2017,2020))]
kern_history_pEPA_reg(sub)


    ## Stonehosue vs Kern (17-19) - pEPA regressions <--- not too useful, focus on table
sub = sub[sub.punter_player_name == 'B.Kern']
stone = data[data.punter_player_name == 'R.Stonehouse']
sub = pd.concat([sub, stone])
kern_stone_pEPA_reg(sub, 'ea_punt_epa_above_expected')
kern_stone_pEPA_reg(sub, 'SHARP_RERUN')


    ## Stonehouse vs NFL 2022
data = data[data.season == 2022]
stone_nfl_pEPA_reg(data)

# Individual Punter Plots
p = Path(Path.cwd(), 'processed data', 'percentiles_other_2022.json')
with open(p, 'r') as file:
    measures = json.loads(file.read())
check = measures.pop('check')
punters = measures.pop('punters')
teams = measures.pop('teams')
# measures = {key:np.array(val) for key,val in measures.items()} 
del measures


test = pd.DataFrame()
k = 1
for val in data.punter_player_name.unique():
    sub = data[data.punter_player_name == val]
    if sub.shape[0] >= 30: # 30 PUNT MINIMUM FOR PUNTER FOR SEASON
        test.loc[k,'name'] = val
        test.loc[k,'team'] = teams[val]
        test.loc[k,'color'] = sub.team_color.value_counts().index[0]
        test.loc[k,'c2'] = sub.team_color2.value_counts().index[0]
        
        test.loc[k,'punts'] = int(sub.shape[0])
        test.loc[k,'return_rate'] = sub.returned.mean()
        test.loc[k,'return_yds'] = sub.return_yards_r.mean()
        test.loc[k,'gross'] = sub.GrossYards.mean()
        test.loc[k,'norm_net'] = np.mean(sub.NetYards/sub.yardline_100)
        test.loc[k,'SHARP_RERUN'] = sub.SHARP_RERUN.mean()
        test.loc[k,'SHARP_RERUN_OF'] = sub.SHARP_RERUN_OF.mean()
        test.loc[k,'SHARP_RERUN_PD'] = sub.SHARP_RERUN_PD.mean()
        test.loc[k,'YardLineAfter_For_Opponent'] = sub.SHARP_RERUN_PD.mean()
        test.loc[k,'yardline_100'] = sub.yardline_100.mean()       
        test.loc[k,'pEPA'] = sub.ea_punt_epa_above_expected.mean()
        k+=1
        
for val in ['punts','return_yds','YardLineAfter_For_Opponent','yardline_100']:
    test[val] = test[val].astype('int')
    

individual_punter_adv(test, 'SHARP_RERUN', 'pEPA', 'SRR_pEPA', 
                      'SHARP RERUN aka Adj Net*', 'Punt EPA*')    

individual_punter_adv(test, 'SHARP_RERUN_OF', 'SHARP_RERUN_PD', 'nSRR-OF_PD', 
                      'Open Field Adj. Net*', 'Pin Deep Adj. Net*')   

individual_punter_adv(test, 'yardline_100', 'YardLineAfter_For_Opponent', 'YTG_OppYL', 
                      'Yards to go', 'Resulting Opponent YTG')  

individual_punter_adv(test, 'return_rate', 'return_yds', 'Return-Rate_Yd', 
                      'Return Rate', 'Return Yd Allowed') 

individual_punter_adv(test, 'gross', 'return_yds', 'test', 
                      'Gross Yards', 'Return Yd Allowed')   

individual_punter_adv(test, 'norm_net', 'pEPA', 'Norm-Net_pEPA', 
                        'Normalized Net', 'Punt EPA*')     
    
individual_punter_adv(test, 'norm_net', 'SHARP_RERUN', 'Norm-Net_SRR', 
                        'Normalized Net', 'Adj. Net*')     
    
individual_punter_adv(test, 'return_rate', 'SHARP_RERUN', 'Return-Rate_SRR', 
                      'Return Rate', 'Adj. Net*')