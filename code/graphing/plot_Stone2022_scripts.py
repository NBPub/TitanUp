import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects 
import pandas as pd
import numpy as np

# Part III, punt data = 2022 punt data / teams / punters / R.Stonehouse <-- Punter to analyze
def punt_att_KDE(punts): # Punt Attempts vs Yds to go (KDE)
    settings = {'figure.figsize':[12, 8], 'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
      'axes.grid':False,'axes.labelweight':'bold','axes.titleweight':'bold', 'axes.titlesize':'x-large','axes.labelsize':'x-large',
      'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 'savefig.dpi': 300, 'savefig.bbox':'tight'}   
        
    with plt.rc_context(settings):
        sns.kdeplot(data=punts, x="yardline_100", hue = 'POI', legend=False,
                    common_norm=False, fill=True, alpha=0.2, linewidth=8)
        plt.xlabel('Yards to go')
        plt.ylabel('Estimation of Punt Probability')
        plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
        plt.legend(['R.Stonehouse','Rest of NFL'], labelcolor=['darkorange','royalblue'], frameon=False, loc='upper left', fontsize='xx-large')
        plt.savefig('graphs/stonehouse/punt_kde_2022.png')
        # plt.show()
        plt.close()   
        
def punt_att_swarm(punts, teams, analyze): # Punter Attempts across League (boxen + swarm)
    plot_settings = {'figure.figsize':[12, 8],'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
      'axes.grid':True, 'grid.color':'dimgrey','axes.grid.axis':'x','axes.labelweight':'bold','axes.titleweight':'bold', 'axes.titlesize':'x-large',
      'grid.alpha':0.5, 'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 
      'savefig.dpi': 300, 'savefig.bbox':'tight'}    
    wer = pd.DataFrame(punts.value_counts('punter_player_name'))
    for val in wer.index:
        wer.loc[val,'team'] = teams[val]
    
    with plt.rc_context(plot_settings):
        sns.boxplot(x=wer[0])
        ax = sns.swarmplot(data=wer, x=0, hue=0, size=35, palette='flare', legend=False, edgecolor = 'k', linewidth=3)
        plt.xlabel('Punt Attempts for each Punter')
        # Stonehouse Label
        plt.annotate(f'{analyze}\n{wer.loc[analyze,0]}', (wer.loc[analyze,0],-0.1), ha='left', color='purple', fontsize='x-large')
        
        # Teams with multiple punters
        x = wer.team.value_counts()
        x = x[x>1] 
        if x.shape[0]>0:
            plt.text(wer.min()[0], -.43,'Teams with multiple Punters', ha='left')
            for i,val in enumerate(x.index):       
                plt.text(wer.min()[0], -.4+0.03*i,f'{val} ({x[val]})', ha='left')
    
        # team names in circle
        colors = ax.collections[0].get_facecolors()
        colors = abs(colors - np.concatenate((np.ones((colors.shape[0],3)), np.zeros((colors.shape[0],1))), axis=1))
        for i,val in enumerate(ax.collections[0].get_offsets()):
            team = wer.team[i]
            correct = -1 if team in [] else 1  # reverse certain team labels
            # correct = 1
            plt.annotate(team,(val[0], 1.15*val[1]*correct), ha='center', va='center', color=tuple(colors[i]))
            #named.append(teams[wer.index[i]])
        

        plt.savefig('graphs/stonehouse/punt_counts_2022.png')
        # plt.show()
        plt.close()
        
def punt_distance_boxen(punts, analyze):
    sub = punts.loc[:,['kick_distance','net_yards','POI','yardline_100', 'punter_player_name']]
    sub.loc[:,'kick_distance'] = sub.kick_distance/sub.yardline_100
    sub.loc[:,'net_yards'] = sub.net_yards/sub.yardline_100
    
    plot_settings = {'figure.figsize':[8, 12],'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
      'axes.grid':True, 'grid.color':'dimgrey','axes.grid.axis':'x','axes.labelweight':'bold','axes.titleweight':'bold', 'axes.titlesize':'x-large',
      'grid.alpha':0.5, 'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 
      'savefig.dpi': 300, 'savefig.bbox':'tight'}    
    
    
    with plt.rc_context(plot_settings):
        plt.subplot(2,1,2)
        sns.boxenplot(data = sub,  x ='net_yards', y = 'POI')
    
        plt.text(sub[sub.punter_player_name==analyze].net_yards.mean(),1,
                 f'{"{:.2f}".format(sub[sub.punter_player_name==analyze].net_yards.mean())}\navg', ha='right')
        plt.text(sub[sub.punter_player_name!=analyze].net_yards.mean(),0,
                 f'{"{:.2f}".format(sub[sub.punter_player_name!=analyze].net_yards.mean())}\navg', ha='right')
        
        
        # Number of punts
        plt.text(sub.net_yards.max()*-.1,1,
             analyze, ha='center', color='salmon')      
        plt.text(sub.net_yards.max()*-.1,0.9,
             f'{sub[sub.punter_player_name==analyze].shape[0]} punts', ha='center')      
        
        plt.text(sub.net_yards.max()*-.1,0.05,
             'Rest of NFL', ha='center', color='royalblue')       
        plt.text(sub.net_yards.max()*-.1,-0.1,
             f'{sub[sub.punter_player_name!=analyze].shape[0]} punts', ha='center')   
    
        plt.axis([sub.net_yards.min(), sub.net_yards.max(), -0.5, 1.5])
        plt.xlabel('Net Yards / Yards to go', fontsize='x-large')
        plt.ylabel('')
        plt.yticks([])

        plt.subplot(2,1,1)
        sns.boxenplot(data = sub, x ='kick_distance', y = 'POI')
        
        plt.text(sub[sub.punter_player_name==analyze].kick_distance.mean(),1,
                 f'{"{:.2f}".format(sub[sub.punter_player_name==analyze].kick_distance.mean())}\navg', ha='right')
        plt.text(sub[sub.punter_player_name!=analyze].kick_distance.mean(),0,
                 f'{"{:.2f}".format(sub[sub.punter_player_name!=analyze].kick_distance.mean())}\navg', ha='right')
        
        # Number of punts
        plt.text(sub.kick_distance.max()*.2,1,
             analyze, ha='center', color='salmon')      
        plt.text(sub.kick_distance.max()*.2,0.9,
             f'{sub[sub.punter_player_name==analyze].shape[0]} punts', ha='center')      
        
        plt.text(sub.kick_distance.max()*.2,0.05,
             'Rest of NFL', ha='center', color='royalblue')       
        plt.text(sub.kick_distance.max()*.2,-0.1,
             f'{sub[sub.punter_player_name!=analyze].shape[0]} punts', ha='center')   
        
        plt.axis([sub.kick_distance.min(), sub.kick_distance.max(), -0.5, 1.5])
        plt.xlabel('Gross Yards / Yards to go', fontsize='x-large')
        plt.ylabel('')
        plt.yticks([])
        
        plt.savefig('graphs/stonehouse/stonehouse_nfl_box.png')
        # plt.show()
        plt.close()
        
def punt_distance_reg(punts):
    # data prep to get subplots for lmplot
    da = punts.loc[:,['yardline_100','kick_distance','net_yards','POI']]
    del punts
    half = da.shape[0]
    da2 = pd.concat([da,da]).reset_index(drop=False)
    del da
    da2.loc[0:half-1,'punt_yd'] = da2.loc[0:half-1,'kick_distance']
    da2.loc[0:half-1,'Type'] = 'Gross'
    da2.loc[half:,'punt_yd'] = da2.loc[half:,'net_yards']
    da2.loc[half:,'Type'] = 'Net'
    da2.drop(columns = ['index','kick_distance','net_yards'], inplace=True)  
    
    settings = {'figure.figsize':[12, 8],'figure.facecolor':'gainsboro', 'figure.edgecolor':'k',  \
      'axes.grid':True, 'grid.color':'dimgrey','axes.grid.axis':'both','axes.labelweight':'bold','axes.titleweight':'bold', 'axes.titlesize':'x-large',
      'grid.alpha':0.5, 'xtick.color':'k', 'xtick.labelsize': 'large', 'font.weight':'bold', 
      'savefig.dpi': 300, 'savefig.bbox':'tight'}       
    
    with plt.rc_context(settings):
        g = sns.lmplot(data = da2, x = 'yardline_100', y = 'punt_yd', hue='POI', scatter=False, col='Type', legend=False,
                       line_kws={'lw':5},facet_kws={'legend_out':False}, order=3)
        g.set_titles(col_template='Punts - {col_name}')
        g.set_xlabels('Yards to go')
        g.set_ylabels('Punt Yards')
    
        for ax in g.axes.ravel():
            ax.legend(labelcolor=['royalblue','darkorange'], frameon=False, loc='upper left')
            ax.plot([37,70],[37,70],'k--', lw=1)
            ax.set_xlabel('Yards to go')    
        
        
        plt.tick_params(axis='y',labelleft=True, pad=0)
        plt.savefig('graphs/stonehouse/stonehouse_nfl_reg.png')
        # plt.show()
        plt.close()
        
def individual_punter_reg(data, col1, col2, savename): # table data, x column, y column
    settings = {'figure.figsize':[8, 8], 'figure.facecolor':'#232323', 'figure.edgecolor':'w',  \
  'axes.titlecolor':'w','axes.labelcolor':'w','axes.edgecolor':'w', 'xtick.color':'w','ytick.color':'w',
  'axes.grid':False,'axes.labelweight':'bold','axes.titleweight':'bold', 'axes.titlesize':'x-large','axes.labelsize':'x-large',
  'ytick.labelsize':'large', 'xtick.labelsize': 'large', 'font.weight':'bold', 'savefig.dpi': 300, 'savefig.bbox':'tight'}   

    # axes names
    ax_labels = {'norm_net':'Net Yards / Yards to go', 'norm_gross':'Gross Yards / Yards to go',
                 'return_rate':'Return Rate', 'YTG':'Avg. Yards to go','OOB':'Out-of-bounds Rate',
                 'in20': 'Inside 20 Rate'}
    
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
    
        plt.xlabel(ax_labels[col1])
        plt.ylabel(ax_labels[col2])
        
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
        plt.savefig(f'graphs/stonehouse/{savename}')
    # plt.show()
    plt.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    