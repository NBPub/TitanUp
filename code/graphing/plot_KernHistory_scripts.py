import seaborn as sns
import matplotlib.pyplot as plt
# import matplotlib.patheffects as path_effects 
import matplotlib.ticker as mtick
import pandas as pd
# import numpy as np

# Return rate comes from other script (plot_Punts)

# KDE
def punt_att(punts, years):
    sub= punts[punts.season.isin([val for val in range(years[0],years[1])])]    
    
    settings = {'figure.figsize':[12, 8], 'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
  'axes.grid':False,'axes.labelweight':'bold','axes.titleweight':'bold', 'axes.titlesize':'x-large','axes.labelsize':'x-large',
  'grid.alpha':0.5, 'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 'savefig.dpi': 300, 'savefig.bbox':'tight'}   

    with plt.rc_context(settings):
        sns.kdeplot(data=sub, x="yardline_100", hue = 'punter_player_name', 
                    legend=True,hue_order=['Rest of NFL', 'B.Kern'],
                    common_norm=False, fill=True, alpha=0.3, linewidth=5)
        plt.xlabel('Yards to go')
        plt.ylabel('Estimation of Punt Probability')
        plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
        plt.legend(['B.Kern','Rest of NFL'], labelcolor=['darkorange','royalblue'], 
                   frameon=False, loc='upper left', fontsize='xx-large')
        plt.savefig('graphs/kern history/Attempts-v-ToGo.png')
        # plt.show()
        plt.close() 

# OOB/YTG vs year, boxen
def year_boxen(punts, metric, years): # years should be 2014 - 2022, 2016-2022
    sub= punts[punts.season.isin([val for val in range(years[0],years[1])])]
   
    settings = {'figure.figsize':[12, 8], 'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
    'axes.grid':True,'axes.grid.axis':'x',
    'axes.labelweight':'bold','axes.titleweight':'bold', 'axes.titlesize':'x-large','axes.labelsize':'x-large',
    'grid.alpha':0.5, 'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 'savefig.dpi': 300, 'savefig.bbox':'tight'}      
    with plt.rc_context(settings):
        sns.boxenplot(data=sub,y=sub[metric]/sub.yardline_100, x='season', hue='punter_player_name',
                     hue_order=['Rest of NFL', 'B.Kern'],)
        
        plt.xlabel('Season')
        if metric == 'punt_out_of_bounds':
            plt.legend(loc='upper right', frameon=False, fontsize='x-large', 
                       labelcolor=['royalblue','darkorange',])
            plt.ylabel('Out of bounds / Yards to go')
            plt.savefig('OOB-Boxen.png')
        else:
            plt.ylim([0,1.1])
            plt.legend(loc='upper center', frameon=False, fontsize='x-large', 
                       labelcolor=['royalblue','darkorange',])
            plt.ylabel('graphs/kern history/Net Yards / Yards to go')
            
            plt.savefig('graphs/kern history/NetYds-Boxen.png')            
        # plt.show() 
        plt.close() 

    # LM Plots (BIG GRIDS)
# Punt Distance Regressions (13x2)
def punt_distance_reg(punts):
    half = punts.shape[0]
    da2 = pd.concat([punts,punts]).reset_index(drop=True) 
    da2.loc[0:half-1,'punt_yd'] = da2.loc[0:half-1,'kick_distance']
    da2.loc[0:half-1,'Type'] = 'Gross'
    da2.loc[half:,'punt_yd'] = da2.loc[half:,'net_yards']
    da2.loc[half:,'Type'] = 'Net'
    da2.drop(columns = ['kick_distance','net_yards'], inplace=True)    

    settings = {'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',
      'axes.grid':True, 'grid.color':'dimgrey','axes.grid.axis':'both','axes.labelweight':'bold', 
      'axes.titleweight':'bold', 'axes.titlesize':'x-large', 'grid.alpha':0.5, 'xtick.color':'k', 
      'font.weight':'bold', 'savefig.dpi': 300,'axes.formatter.limits':(-1,4),               }        
    with plt.rc_context(settings):
        g = sns.lmplot(data = da2, x = 'yardline_100', y = 'punt_yd', hue='punter_player_name',
                hue_order=['Rest of NFL', 'B.Kern'], scatter=False, col='Type', 
                legend=False, row='season', order=3,
                line_kws={'lw':5, 'scaley':True,'label':['Kern','NFL']},
                facet_kws={'legend_out':False,'sharex':False, 'gridspec_kws':{'wspace':0.1}
                         })
        g.set_ylabels('Punt Yards')
        g.set(xlim=(25,95),ylim=(10,60))   
        for ax in g.axes.ravel():
            ax.legend(labelcolor=['royalblue','darkorange'], frameon=False, loc='lower right')
            ax.plot([26,74],[26,74],'k--', lw=1)
            ax.set_xlabel('Yards to go')    
        g.tick_params(axis='y',labelleft=True, pad=0)     
        g.set_titles(template='{row_name} - {col_name} yards')
        
        plt.savefig('graphs/kern history/GrossNetvToGo_Reg.png')            
        # plt.show()
        plt.close()    

# Binary Regressions (13x5)
def binary_reg(punts):
    half = punts.shape[0]
    da2 = pd.concat([punts,]*5).reset_index(drop=True)
    for i,val in enumerate(['punt_inside_twenty','touchback','punt_out_of_bounds','punt_downed','punt_fair_catch']):
        da2.loc[i*half:(i+1)*half-1, 'metric'] = da2.loc[i*half:(i+1)*half-1, val]
        da2.loc[i*half:(i+1)*half-1, 'type'] = val.replace('punt_','').replace('_',' ').capitalize()
    da2.drop(columns = ['punt_inside_twenty','touchback','punt_out_of_bounds','punt_downed','punt_fair_catch'], inplace=True)
    
    settings = {'figure.figsize':[12, 8],'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
      'axes.grid':True, 'grid.color':'dimgrey','axes.grid.axis':'both','axes.labelweight':'bold','axes.titleweight':'bold', 'axes.titlesize':'x-large',
      'grid.alpha':0.5, 'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 'savefig.dpi': 300}          
    with plt.rc_context(settings):
        g = sns.lmplot(data = da2, x = 'yardline_100', y = 'metric', hue='punter_player_name',hue_order=['Rest of NFL', 'B.Kern'],
                       scatter=False, col='type', legend=False,  row='season', order=1,
                       line_kws={'lw':5, 'scaley':True,'label':['Kern','NFL']},
                       facet_kws={'legend_out':False,'sharex':False,'sharey':False,
                                   'gridspec_kws':{'wspace':0.15, 'hspace':0.25}, 
                         })

        g.set_ylabels('Percentage')
    
        for ax in g.axes.ravel():
            ax.legend(labelcolor=['royalblue','darkorange'], frameon=False, loc='upper center')
            ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
            ax.set_xlabel('Yards to go')           
        g.set_titles(template='{row_name} - {col_name}')
    
        plt.savefig('graphs/kern history/binaries_Reg.png')
        # plt.show()
        plt.close()

# EPA/WPA Regressions (13x2)
def xPA_reg(punts):
    half = punts.shape[0]
    da2 = pd.concat([punts,punts]).reset_index(drop=True) 
    da2.loc[0:half-1,'xPA'] = da2.loc[0:half-1,'epa']
    da2.loc[0:half-1,'Type'] = 'EPA'
    da2.loc[half:,'xPA'] = da2.loc[half:,'wpa']
    da2.loc[half:,'Type'] = 'WPA'
    da2.drop(columns = ['epa','wpa'], inplace=True) 

    settings = {'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',
      'axes.grid':True, 'grid.color':'dimgrey','axes.grid.axis':'both','axes.labelweight':'bold', 
      'axes.titleweight':'bold', 'axes.titlesize':'x-large', 'grid.alpha':0.5, 'xtick.color':'k', 
      'font.weight':'bold', 'savefig.dpi': 300,'axes.formatter.limits':(-1,4),               }        
    with plt.rc_context(settings):
        g = sns.lmplot(data = da2, x = 'yardline_100', y = 'xPA', hue='punter_player_name',
                hue_order=['Rest of NFL', 'B.Kern'], scatter=False, col='Type', 
                legend=False, row='season', line_kws={'lw':5, 'scaley':True,'label':['Kern','NFL']},
                facet_kws={'legend_out':False,'sharex':False,'sharey':False,
                            'gridspec_kws':{'wspace':0.15, 'hspace':0.25}, 
                     })
        g.set_ylabels('EP or WP Added')  
        for ax in g.axes.ravel():
            ax.legend(labelcolor=['royalblue','darkorange'], frameon=False, loc='upper center')
            ax.set_xlabel('Yards to go')   
        g.set_titles(template='{row_name} - {col_name}')
        
        plt.savefig('graphs/kern history/xPAvToGo_Reg.png')           
        # plt.show()
        plt.close()  