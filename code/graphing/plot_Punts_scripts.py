import seaborn as sns
import matplotlib.pyplot as plt
# import matplotlib.patheffects as path_effects 
# import matplotlib.ticker as mtick
# import pandas as pd
import numpy as np

def punt_distance_reg_order(punts, metric):
    plt.figure(figsize=(6,4), facecolor='gainsboro')
    ax = sns.barplot(data=punts, x='yardline_100', y=metric, width=4, errwidth=0.2, color='k', errcolor='magenta', alpha=0.4)   
    
    bounds = ax.get_xbound()
    ax.set_xlim(bounds[0]+12,bounds[1]) 
    ax.set_xticks(np.arange(bounds[0]+0.5, bounds[1]-0.5, 5, dtype='int'))
    
    adjust =  ax.get_xticklabels()[0].get_position()[0] - int(ax.get_xticklabels()[0].get_text())
    upper = ax.get_ybound()[1]
    
    sns.regplot(x=punts.yardline_100+adjust, y=punts[metric], scatter=False,
               order=1, truncate=True, line_kws={'alpha':0.8, 'lw':6, 'ls':'--'})
    sns.regplot(x=punts.yardline_100+adjust, y=punts[metric], scatter=False,
               order=2, truncate=True, line_kws={'alpha':0.8, 'lw':6, 'ls':'--'})
    sns.regplot(x=punts.yardline_100+adjust, y=punts[metric], scatter=False,
               order=3, truncate=True, line_kws={'alpha':0.8, 'lw':6, 'ls':'--'})
        
    plt.text(15,upper*0.96,'1st order',color='royalblue', fontsize='large', fontweight='bold', ha='center')
    plt.text(15,upper*0.88,'2nd order',color='darkorange', fontsize='large', fontweight='bold', ha='center')
    plt.text(15,upper*0.80,'3rd order',color='green', fontsize='large', fontweight='bold', ha='center')
    ax.set_xlabel('Yards to go', labelpad=1)    
    if metric == 'kick_distance':
        ax.set_ylabel('Punt Yds - Gross', fontweight='bold',fontsize='large')
        plt.savefig('graphs/Intro/gross_yds_curvefit',dpi=300,bbox_inches='tight')
    else:
        ax.set_ylabel('Punt Yds - Net', fontweight='bold',fontsize='large', color='teal')
        plt.savefig('graphs/Intro/net_yds_curvefit',dpi=300,bbox_inches='tight') 
    # plt.show()
    plt.close()

def punt_att(xdata):
    settings = {'figure.figsize':[6, 6],'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
  'axes.grid':True, 'grid.color':'dimgrey','axes.grid.axis':'x','axes.labelweight':'bold','axes.labelsize':'x-large',
  'grid.alpha':0.5, 'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 
  'savefig.dpi': 300, 'savefig.bbox':'tight'}  

    with plt.rc_context(settings):
        sns.histplot(x=xdata, kde=True, color='green', bins=15, 
                     line_kws={'ls':'-','lw':6, 'alpha':0.7})
        plt.grid(axis='x', alpha=0.5)
        plt.title('Distribution of punt attempts\nby distance, from 2009-2022', y=0.9, loc='left')
        plt.ylabel('Punts')
        plt.xlabel('Yards to go')
    
        plt.savefig('graphs/Intro/distribution.png',dpi=300,bbox_inches='tight')
        # plt.show()
    plt.close()
    
def punt_distance_bar(punts, percent_lines):
    plt.figure(figsize=(6,4), facecolor='gainsboro')
    sns.barplot(data=punts, x='yardline_100', y='kick_distance', width=4, errwidth=0.8, color='k', errcolor='magenta', alpha=0.6)
    ax = sns.barplot(data=punts, x='yardline_100', y='net_yards', width=4, errwidth=1.2, color='teal', errcolor='lightblue', alpha=0.3)
    bounds = ax.get_xbound()
    
    ax.set_xlim(bounds[0]+12,bounds[1])
    bounds = ax.get_xbound()     
    ax.set_xticks(np.arange(bounds[0]+0.5, bounds[1]-0.5, 5, dtype='int'))    
    ax.set_ylim(25,55)
    
    adjust =  ax.get_xticklabels()[0].get_position()[0] - int(ax.get_xticklabels()[0].get_text())
    if percent_lines:
        savename = 'Kern v Stonehouse/bar_punt_yds_percentile.png'
        for i in range(7): # 1.0 down to 0.4, text labels not perfect
            k = 171-i*20
            ax.plot((adjust,72),(0,100-10*i),'--',color=(1,k/255,0))
            ax.text(12+i*3.5,45-i*2.7,round(1-i*0.1,1),color=(1,k/255,0), fontweight='bold')
    else:
        savename = 'Intro/bar_punt_yds.png'
        ax.plot((adjust,72),(0,100),'--',color='blue') # draw 1:1 line only
        ax.text(53+adjust,53, '1:1', fontweight='bold',rotation=45,color='b', va='top')         
        gross = round(punts.kick_distance.mean(),1)
        net = round(punts.net_yards.mean(),1)        
        ax.text(85+adjust,53, f'Gross: {gross}yd avg', fontweight='bold', ha='right')    
        ax.text(85+adjust,51.5, f'Net: {net}yd avg', fontweight='bold', color='teal', ha='right')
           
    ax.set_ylabel('Punt Yds', fontweight='bold',fontsize='large')
    ax.set_xlabel('Yards to go', labelpad=1)    

    
    plt.savefig(f'graphs/{savename}',dpi=300,bbox_inches='tight')
    # plt.show()
    plt.close()
    
def OOB_bar(punts):
    mean = punts.punt_out_of_bounds.mean()   
    plt.figure(figsize=(4,3), facecolor='gainsboro')
    ax = sns.barplot(data=punts, x='yardline_100', y='punt_out_of_bounds', width=4,
                     errwidth=0.5, color='k', errcolor='magenta', alpha=0.6)
    bounds = ax.get_xbound()
    
    ax.set_xlim(bounds[0]+12,bounds[1])
    bounds = ax.get_xbound()     
    ax.set_xticks(np.arange(bounds[0]+0.5, bounds[1]-0.5, 5, dtype='int'))    
    ax.set_ylim(0,.25)
    
    ax.plot(bounds,(mean, mean),'--',color='teal')
    ax.text(bounds[1]*0.6, mean-0.02, f'{round(100*mean,1)}% avg', fontweight='bold', 
            ha='right', fontsize='small', color='teal')
    
    ax.set_title('Out-of-Bounds', y=0.8, loc='center', fontweight='bold')
    ax.set_ylabel('Rate', fontweight='bold',fontsize='large')
    ax.set_xlabel('Yards to go', labelpad=1)
    
    plt.savefig('graphs/Intro/bar_OOB.png',dpi=300,bbox_inches='tight')    
    #plt.show()
    plt.close()
    
def epa_bar(punts):   
    plt.figure(figsize=(4,3), facecolor='gainsboro')
    ax = sns.barplot(data=punts, x='yardline_100', y='epa', width=4, errwidth=0.5, color='k', errcolor='magenta', alpha=0.6)
    bounds = ax.get_xbound()    
    ax.set_xlim(bounds[0]+12,bounds[1])
    bounds = ax.get_xbound()     
    ax.set_xticks(np.arange(bounds[0]+0.5, bounds[1]-0.5, 5, dtype='int'))
    ax.set_ylim(-.5,.5)
    offset = bounds[1]-100
    
    # fill colors, get means for each bin then collapse. could improve
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
            ax.fill_between((val+offset,keys[i+1]+offset),-0.5,0, color='red',alpha=0.15)
        else:
            ax.fill_between((val+offset,keys[i+1]+offset),0,0.5, color='seagreen',alpha=0.15)
    ax.set_title('Punt EPA vs Yds to go', y=0.8, loc='center', fontweight='bold')
    ax.set_ylabel('EPA', fontweight='bold',fontsize='large')
    ax.set_xlabel('Yards to go', labelpad=1)
    
    plt.savefig('graphs/Intro/bar_EPA.png',dpi=300,bbox_inches='tight')
    #plt.show()
    plt.close()


def two_bar(punts, metrics, scale, savename):
    fig, axes = plt.subplots(2,1, figsize=(4,6), facecolor='gainsboro')
    for i in range(2):
        fancy = metrics[i].replace('punt_','').replace('_',' ').title()
        mean = punts[metrics[i]].mean()
        
        sns.barplot(data=punts, x='yardline_100', y=metrics[i], width=4, errwidth=1, color='k', errcolor='magenta', alpha=0.6, ax=axes[i])
        bounds = axes[i].get_xbound()
    
        axes[i].set_xlim(bounds[0]+12,bounds[1])
        bounds = axes[i].get_xbound()     
        axes[i].set_xticks(np.arange(bounds[0]+0.5, bounds[1]-0.5, 5, dtype='int'))
        
        axes[i].plot(bounds,(mean, mean),'--',color='teal')
        axes[i].text(bounds[1]*0.8, mean+0.02, f'{round(100*punts[metrics[i]].mean(),1)}% avg', fontweight='bold', ha='right', fontsize='small', color='teal')
        axes[i].set_ylim(0,scale)
        
        axes[i].set_title(fancy, y=0.8, loc='center', fontweight='bold')
        axes[i].set_ylabel('Rate', fontweight='bold',fontsize='large')
        axes[i].set_xlabel('Yards to go', labelpad=1)
    
    plt.savefig(f'graphs/Intro/{savename}',dpi=300,bbox_inches='tight')
    # plt.show()
    plt.close()    

def binary_LogReg(punts, metrics):
    # Hard Code text, yscale settings for now
    settings = {'figure.figsize':[4, 5],'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
      'axes.grid':True, 'grid.color':'dimgrey','axes.grid.axis':'both','axes.labelweight':'bold','axes.labelsize':'x-large',
      'grid.alpha':0.3, 'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 
      'savefig.dpi': 300, 'savefig.bbox':'tight'}  
    with plt.rc_context(settings):
        for val in metrics:
            sns.regplot(data=punts, x='yardline_100', y=val, scatter=False,
                       truncate=True, logistic=True)
        
        if len(metrics) == 2:
            plt.axis([40,90,0,1])
            plt.text(56,0.6,'Inside Twenty',color='royalblue',fontweight='bold')
            plt.text(48,0.4,'Fair Catch',color='darkorange',fontweight='bold')
            savename = 'LogReg_FC-In20.png'
        else:
            plt.axis([40,90,0,0.35])
            plt.text(80,0.11,'OOB',color='royalblue',fontweight='bold')
            plt.text(42,0.3,'Touchback',color='darkorange',fontweight='bold')
            plt.text(59,0.15,'Downed',color='green',fontweight='bold')
            savename = 'LogReg_others.png'
    
        plt.ylabel('Rate')
        plt.xlabel('Yards to go')
        plt.savefig(f'graphs/Intro/{savename}')
        # plt.show()
        plt.close()


def KernReturn_LogReg(sub, divider, metric):
    settings = {'figure.figsize':[4, 5],'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
      'axes.grid':True, 'grid.color':'dimgrey','axes.grid.axis':'both','axes.labelweight':'bold','axes.labelsize':'x-large',
      'grid.alpha':0.3, 'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 
      'savefig.dpi': 300, 'savefig.bbox':'tight'}      
    with plt.rc_context(settings):
        
        sns.regplot(data=sub[(sub.punter_player_name != 'B.Kern')  & (sub.season < 2022)], 
                    x='yardline_100', y=metric, scatter=False, logistic=True, truncate=True)
        
        sns.regplot(data=sub[(sub.punter_player_name == 'B.Kern') & (sub.season < divider+1)], 
                    x='yardline_100', y=metric, scatter=False, logistic=True, truncate=True)
        
        sns.regplot(data=sub[(sub.punter_player_name == 'B.Kern') & (sub.season > divider) & (sub.season < 2022)],
                    x='yardline_100', y=metric, scatter=False,logistic=True, truncate=True)
              
        plt.xlabel('Yards to go')
        if metric == 'punt_returned':
            plt.ylabel('Return Rate')
            plt.axis([40,90,0,1])
            plt.text(50,0.85,"NFL -09-21",color='royalblue',fontweight='bold')
            plt.text(50,0.8,"Kern -09-16",color='darkorange',fontweight='bold')
            plt.text(50,0.75,"Kern -17-21",color='green',fontweight='bold')  
            plt.savefig('graphs/kern history/LogReg_Kern-returns.png')
        else:
            plt.ylabel('OOB Rate')
            plt.axis([40,90,0,0.35])
            plt.text(50,0.32,"NFL -09-21",color='royalblue',fontweight='bold')
            plt.text(50,0.3,"Kern -09-16",color='darkorange',fontweight='bold')
            plt.text(50,0.28,"Kern -17-21",color='green',fontweight='bold')             
            plt.savefig('graphs/kern history/LogReg_Kern-OOB.png')
        #plt.show()
        plt.close()
        
def NormNet_RetRate_historical(test):
    # labels
    stone = test[test.name == 'R.Stonehouse']
    kern = test[test.name == 'B.Kern'].sort_values('norm_net',ascending=False)[0:5]
    kern2 = test[test.name == 'B.Kern'].sort_values('norm_net',ascending=False)[5:]
    
    settings = {'figure.figsize':[10, 8], 'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
      'axes.grid':False,'axes.labelweight':'bold','axes.titleweight':'bold', 'axes.titlesize':'x-large','axes.labelsize':'x-large',
      'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 'savefig.dpi': 300, 'savefig.bbox':'tight'}   
            
    with plt.rc_context(settings):
        ax = sns.regplot(data=test,x='return_rate',y='norm_net', scatter_kws={'alpha':0.5}, color='grey')
        sns.regplot(data=test[test.name == 'B.Kern'],x='return_rate',y='norm_net', scatter_kws={'alpha':0.75}, color='magenta')
        ax.plot(stone['return_rate'],stone['norm_net'],'o', color='orange')
        bounds = (ax.get_xlim(), ax.get_ylim())
        
        ax.plot((test['return_rate'].mean(),test['return_rate'].mean()),bounds[1],'--',color='grey',lw=0.5)
        ax.plot(bounds[0],(test['norm_net'].mean(),test['norm_net'].mean()),'--',color='grey',lw=0.5)
        
        ax.set_xlim(bounds[0])
        ax.set_ylim(bounds[1])
                    
        plt.annotate('R.Stonehouse', (stone['return_rate'],stone['norm_net']+.005), ha='center',va='bottom', color='darkorange', fontweight='bold', fontsize='large')
        plt.text(0.3,0.705,'B.Kern', color='magenta',fontsize='large')
        for val in kern.index:
            plt.annotate(kern.season[val], (kern['return_rate'][val],kern['norm_net'][val]), ha='right',va='bottom', color='magenta', fontweight='bold')
        for val in kern2.index:
            plt.annotate(kern2.season[val], (kern2['return_rate'][val],kern2['norm_net'][val]), ha='left',va='top', color='magenta', fontweight='bold')    
        plt.text(0.45,0.7,f"NFL('09-'22)\n{test.shape[0]} punter seasons", color='grey',fontsize='large')
        
        plt.xlabel('Return Rate')
        plt.ylabel('Net Yards / Yards to go')
        plt.savefig('graphs\kern v stonehouse\historical-normnet-v-returnrate.png')
        
    plt.show()
    plt.close()    
