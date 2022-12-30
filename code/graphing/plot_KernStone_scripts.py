import seaborn as sns
import matplotlib.pyplot as plt
# import matplotlib.patheffects as path_effects 
import matplotlib.ticker as mtick
import pandas as pd
# import numpy as np

# Part II, punt data = 2009-2022 punt data / R.Stonehouse, B.Kern as titans <-- Punters to analyze
def punt_att_KDE(punts): # Punt Attempts vs Yds to go (KDE)
    settings = {'figure.figsize':[12, 8], 'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
      'axes.grid':False,'axes.labelweight':'bold','axes.titleweight':'bold', 'axes.titlesize':'x-large','axes.labelsize':'x-large',
      'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 'savefig.dpi': 300, 'savefig.bbox':'tight'}   
    with plt.rc_context(settings):
        sns.kdeplot(data=punts, x="yardline_100", hue = 'punter_player_name', legend=True,
                    common_norm=False, fill=True, alpha=0.2, linewidth=8, palette='Accent_r')
        plt.xlabel('Yards to go')
        plt.ylabel('Estimation of Punt Probability')
        plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
        plt.legend(['R.Stonehouse', 'B.Kern'], labelcolor=['orange','deeppink'], frameon=False, loc='upper left', fontsize='xx-large')
        
        plt.savefig('graphs/kern v stonehouse/kde.png')
        # plt.show()
        plt.close() 
        
def punt_distance_boxen(punts):
    sub = punts.loc[:,['kick_distance','net_yards','yardline_100', 'punter_player_name']]
    sub.loc[:,'kick_distance'] = sub.kick_distance/sub.yardline_100
    sub.loc[:,'net_yards'] = sub.net_yards/sub.yardline_100
    
    settings = {'figure.figsize':[8, 12],'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
      'axes.grid':True, 'grid.color':'dimgrey','axes.grid.axis':'x','axes.labelweight':'bold','axes.titleweight':'bold', 'axes.titlesize':'x-large',
      'grid.alpha':0.5, 'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 
      'savefig.dpi': 300, 'savefig.bbox':'tight'}    
    with plt.rc_context(settings):
        plt.subplot(2,1,2)
        sns.boxenplot(data = sub,  x ='net_yards', y = 'punter_player_name', palette='Accent_r', linewidth=3)
        colors = ['deeppink', 'orange']
        # Label Mean
        placement = sub.net_yards.max()*.25
        for i,val in enumerate(sub.punter_player_name.unique()): 
            number1 = sub[sub.punter_player_name==val].net_yards.mean()
            number2 = sub[sub.punter_player_name==val].shape[0]
            plt.text(number1,i, f'{"{:.2f}".format(number1)}\navg', ha='right', color='grey')
            plt.text(placement,i+.07, f'{number2} punts', ha='center', color='grey')
            plt.text(placement,i+.15, val, ha='center', color=colors[i])
       
        plt.axis([sub.net_yards.min(), sub.net_yards.max(), -0.5, 1.5])
        plt.xlabel('Net Yards / Yards to go', fontsize='x-large')
        plt.ylabel('')
        plt.yticks([])

        plt.subplot(2,1,1)
        sns.boxenplot(data = sub, x ='kick_distance', y = 'punter_player_name', palette='Accent_r', linewidth=3)        
        # Label Mean, # Punts
        placement = sub.kick_distance.max()*.25
        for i,val in enumerate(sub.punter_player_name.unique()): 
            number1 = sub[sub.punter_player_name==val].kick_distance.mean()
            number2 = sub[sub.punter_player_name==val].shape[0]
            plt.text(number1,i, f'{"{:.2f}".format(number1)}\navg', ha='right', color='grey')
            plt.text(placement,i+.07, f'{number2} punts', ha='center', color='grey')
            plt.text(placement,i+.15, val, ha='center', color=colors[i])          
    
        plt.axis([sub.kick_distance.min(), sub.kick_distance.max(), -0.5, 1.5])
        plt.xlabel('Gross Yards / Yards to go', fontsize='x-large')
        plt.ylabel('')
        plt.yticks([])
    
        plt.savefig('graphs/kern v stonehouse/distance-boxen.png')
        # plt.show()
        plt.close()
        
def punt_distance_reg(punts):
    sub = punts.loc[:,['kick_distance','net_yards','yardline_100', 'punter_player_name']]
    half = sub.shape[0]
    da2 = pd.concat([sub,sub]).reset_index(drop=True)
    da2.loc[0:half-1,'punt_yd'] = da2.loc[0:half-1,'kick_distance']
    da2.loc[0:half-1,'Type'] = 'Gross'
    da2.loc[half:,'punt_yd'] = da2.loc[half:,'net_yards']
    da2.loc[half:,'Type'] = 'Net'
    da2.drop(columns = ['kick_distance','net_yards'], inplace=True) 
    
    settings = {'figure.figsize':[12, 8], 'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
      'axes.grid':True, 'grid.color':'dimgrey','axes.grid.axis':'both','axes.labelweight':'bold','axes.titleweight':'bold', 'axes.titlesize':'x-large',
      'grid.alpha':0.5, 'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 'savefig.dpi': 300,  'savefig.bbox':'tight'}      
    with plt.rc_context(settings):
        g = sns.lmplot(data = da2, x = 'yardline_100', y = 'punt_yd', hue='punter_player_name', scatter=False, col='Type', legend=False,
                       line_kws={'lw':4},facet_kws={'legend_out':False}, palette='Accent_r', order=3)
        g.set_titles(col_template='Punts - {col_name}')
        g.set_xlabels('Yards to go')
        g.set_ylabels('Punt Yards')
        for ax in g.axes.ravel():
            ax.legend(labelcolor=['deeppink','orange'], frameon=False, loc='upper left')
            ax.plot([33,70],[33,70],'k--', lw=1)
            ax.set_xlabel('Yards to go')    
        plt.tick_params(axis='y',labelleft=True, pad=0)
        
        plt.savefig('graphs/kern v stonehouse/LM-distance.png')
        # plt.show()
        plt.close()

def epa_reg(punts):
    sub = punts.loc[:,['epa','wpa','yardline_100', 'punter_player_name']]
    half = sub.shape[0]
    da2 = pd.concat([sub,sub]).reset_index(drop=True)
    da2.loc[0:half-1,'xPA'] = da2.loc[0:half-1,'epa']
    da2.loc[0:half-1,'Type'] = 'EPA'
    da2.loc[half:,'xPA'] = da2.loc[half:,'wpa']
    da2.loc[half:,'Type'] = 'WPA'
    da2.drop(columns = ['epa','wpa'], inplace=True)
        
    settings = {'figure.figsize':[12, 8], 'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
      'axes.grid':True, 'grid.color':'dimgrey','axes.grid.axis':'both','axes.labelweight':'bold','axes.titleweight':'bold', 'axes.titlesize':'x-large',
      'grid.alpha':0.5, 'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 'savefig.dpi': 300,  'savefig.bbox':'tight'}     
    with plt.rc_context(settings):
        g = sns.lmplot(data = da2, x = 'yardline_100', y = 'xPA', hue='punter_player_name', scatter=False, 
                       col='Type', legend=False, palette='Accent_r',
                       line_kws={'lw':4},facet_kws={'legend_out':False, 'sharey':False})
        g.set_titles(col_template='Punts - {col_name}')
        g.set_xlabels('Yards to go')
        g.set_ylabels('EPA or WPA')
    
        for ax in g.axes.ravel():
            ax.legend(labelcolor=['deeppink','orange'], frameon=False, loc='upper left')
            ax.set_xlabel('Yards to go')    
        plt.tick_params(axis='y',labelleft=True, pad=0)
        
        plt.savefig('graphs/kern v stonehouse/LM-xPA.png')
        # plt.show()
        plt.close()    
    
def binaries_reg(punts):
    half = punts.shape[0]
    da2 = pd.concat([punts,]*5).reset_index(drop=True)
    for i,val in enumerate(['punt_inside_twenty','touchback','punt_out_of_bounds','punt_downed','punt_fair_catch']):
        da2.loc[i*half:(i+1)*half-1, 'metric'] = da2.loc[i*half:(i+1)*half-1, val]
        da2.loc[i*half:(i+1)*half-1, 'type'] = val.replace('punt_','').replace('_',' ').title()
    da2.drop(columns = ['punt_inside_twenty','touchback','punt_out_of_bounds','punt_downed','punt_fair_catch'], inplace=True)
    
    settings = {'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',
      'axes.grid':True, 'grid.color':'dimgrey','axes.grid.axis':'both','axes.labelweight':'bold', 
      'axes.titleweight':'bold', 'axes.titlesize':'x-large', 'grid.alpha':0.5, 'xtick.color':'k', 
      'font.weight':'bold', 'savefig.dpi': 300,  'savefig.bbox':'tight'}    
    with plt.rc_context(settings):
        g = sns.lmplot(data = da2, x = 'yardline_100', y = 'metric', hue='punter_player_name',palette='Accent_r',
                       scatter=False, col='type', legend=False,  
                       line_kws={'lw':5, 'scaley':True,'label':['Kern','NFL']},
                       facet_kws={'legend_out':False,'sharex':False,'sharey':False,
                                   'gridspec_kws':{'wspace':0.15, 'hspace':0.25}, 
                         })

        g.set_ylabels('Percentage')    
        for ax in g.axes.ravel():
            ax.legend(labelcolor=['deeppink','orange'], frameon=False, loc='upper center')
            ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
            ax.set_xlabel('Yards to go')            
        g.set_titles(template='{col_name}')       
        
        plt.savefig('graphs/kern v stonehouse/LM-binaries.png')
        # plt.show()
        plt.close()    