import pandas as pd
from pathlib import Path
import json
pd.options.mode.chained_assignment = None


    # read and clean data
av = pd.read_csv(Path(Path.cwd(),'pbp data','Titans_careerAV.csv'))
av.drop(columns='-9999',inplace=True)

    # Subsets: choose one
# Titans Era, with min Games
sub = av[(av.From > 1996) | (av.To > 1997)]
sub = sub[sub.G>5] # At least 6 games played

# 90s and beyond, top 500 overall (AV at least 5)
# sub = av[av.Rk < 501]
# sub = sub[(sub.From > 1989) | (sub.To > 1990)]


# Add AV per Game column
sub.loc[:,'AV/G'] = 1000*sub.AV/sub.G
del av

    # Group positions, apply manual fixes
# example to help determine player positions with google links, 
# for subset of interest, print table and then print searches for each player
# print(sub[(sub.Pos2 == 'DE') & (sub.Pos == 'OLB') & (sub.Rk >499)]\
#       .sort_values('AV/G', ascending=False))
# for val in sub[(sub.Pos2 == 'DE') & (sub.Pos == 'OLB') & (sub.Rk >499)].Player:
#     print(f'https://www.google.com/search?q={val.replace(" ","+")}') # could add "+NFL" to search

# manual change for Beau Brinkley LSTE -> LS
sub.loc[sub[sub.Player == 'Beau Brinkley'].index,'Pos'] = 'LS'
# fill null Pos
sub.loc[sub[sub.Player == 'Naquan Jones'].index,'Pos'] = 'NT'
sub.loc[sub[sub.Player == 'Byron Stingily'].index,'Pos'] = 'T'
# position groupings
positions = {
    'DE':['LDE','RDE','OLB', 'DL'],
    'DT':['NT','RDT','LDT'],
    'LB':['MLB','ILB','RILB','LILB','ROLB','LOLB', 'LLB','RLB'],
    'S':['SS','FS'],
    'CB':['LCB','RCB','DB'],
    'OL':['C','LT','RT','OT','OG','LG','RG','G','T'],
    'RB':['FB'],
    'ST':['K','P','LSTE', 'LS'],
    'QB':[],'WR':[],'TE':[],
}
# post fixes
fix = {
    'DE':['Brian Orakpo', 'Jason Babin', 'Erik Walden','Sharif Finch', 'Reggie Gilbert', 'Cameron Wake','Shaun Phillips',
         '',''],
    'DT':['Jeffery Simmons', 'Larrell Murchison'],
    'LB':['Zach Cunningham', 'Zaviar Gooden','Joseph Jones', 'Aaron Wallace'],
    'S':['Jordan Babineaux', 'Lance Schulters', "Da'Norris Searcy", 'Lamont Thompson', 'Calvin Lowry',
        'Steve Jackson','Bo Orlando','Perry Phenix','Vincent Fuller','Aric Morris','Anthony Dorsett','Donnie Nickey',
        'Rashad Johnson','Scott McGarrahan','Bobby Myers','Rich Coady','Joe Walker','Daryl Porter','George McCullough',
         'Kevin Kaesviharn','Matthias Farley','Al Afalava','Anthony Smith','Nick Schommer']
}


for key,renames in positions.items():
    sub.loc[sub[sub.Pos==key].index,'Pos2'] = key
    for name in renames:
        sub.loc[sub[sub.Pos==name].index,'Pos2'] = key
        
for pos2, names in fix.items():
    for name in names:
        sub.loc[sub[sub.Player==name].index,'Pos2'] = pos2
        

    # Tables
AV_tables = {}
def ST_positions(v):
    if v['PFR position'] == 'K':
        return ['']+['color:black;background-color:salmon']*4+['']*3
    if v['PFR position'] == 'P':
        return ['']+['color:black;background-color:lightblue']*4+['']*3
    if v['PFR position'] == 'LS':
        return ['']+['color:black;background-color:lightgreen']*4+['']*3


for analyze_position in sub.Pos2.unique():
    table = sub[sub.Pos2==analyze_position].sort_values('AV/G',ascending=False)
    
    # Drop the analyze position column, reorder, rename
    table=table.loc[:,['Rk','Player','Pos','From','To','G','AV','AV/G']]
    table.rename(columns = {'Rk':'Overall Rank','G':'Games','AV/G':'AV per game','Pos':'PFR position'}, inplace=True)
    # set index to overall rank
    # table.set_index('Overall Rank', inplace=True)
    
    # reorder column
    cmap_2 = 'Purples'
    
    # if analyze_position == 'ST':
    #     AV_tables[analyze_position] = \
    #         table.style\
    #             .format_index(lambda v: '')\
    #             .format(formatter="{:.0f}", subset='AV per game')\
    #             .apply(ST_positions, axis=1)\
    #             .background_gradient(cmap='bone_r', vmax=500, subset='Overall Rank')\
    #             .background_gradient(cmap=cmap_2, subset='Games')\
    #             .background_gradient(cmap=cmap_2, subset='AV')\
    #             .background_gradient(cmap=cmap_2, subset='AV per game')\
    #             .set_table_styles([
    #                 {'selector': 'td:hover','props': [('background-color', '#0097A6')]},
    #                 {'selector': 'td, th', 'props': 'font-size:1.1em;'},
    #                 {'selector': 'th', 'props': [('position','sticky'),('top',0)]},
    #                            ])\
    #             .set_table_attributes('class="table table-dark"').to_html()
    # else:
    #     AV_tables[analyze_position] = \
    #         table.style\
    #             .format_index(lambda v: '')\
    #             .format(formatter="{:.0f}", subset='AV per game')\
    #             .background_gradient(cmap='bone_r', vmax=500, subset='Overall Rank')\
    #             .background_gradient(cmap=cmap_2, subset='Games')\
    #             .background_gradient(cmap=cmap_2, subset='AV')\
    #             .background_gradient(cmap=cmap_2, subset='AV per game')\
    #             .set_table_styles([
    #                 {'selector': 'td:hover','props': [('background-color', '#0097A6')]},
    #                 {'selector': 'td, th', 'props': 'font-size:1.1em;'},
    #                 {'selector': 'th', 'props': [('position','sticky'),('top',0)]},
    #                            ])\
    #             .set_table_attributes('class="table table-dark"').to_html()
                

# p = Path(Path.cwd(), 'tables', 'Titans_AV_tables_Titans.json')
# with open(p, 'w', encoding='utf-8') as file:
#     file.write(json.dumps(AV_tables))  
# del AV_tables  
    
    # Analysis for graphs with Top 500, 1990 cutoff
# AV_analysis = {
#     'OL':['Bruce Matthews had an awesome career',
#           'If coaching years were also considered, Munchak would be a little closer',
#           'Some nostalgic names were labelled on the graph'],
#     'QB':['RIP Steve McNair','Interesting that Tannehill and Mariota show similar rate to McNair and Moon.',
#           'Titans legend, Ryan Fitzpatrick!'],
#     'DT':["don't remember Ray Childress",'Jeffery Simmons will be a legend in time, to no suprise',
#           'DaQuan Jones spent a longer time here than I thought'],
#     'RB':['Year selection excludes Earl Campbell', 'CJ2K and Eddie George are legends',
#           'Henry has lower AV per game due to low usage in his early years',          
#           'DeMarco Murray was most of the Titans offense for a time'],
#     'DE':['Exterior DL / EDGE','Brian Orakpo and Jason Babin moved from LB category',
#           'Jurrell Casey was so good for so long! If only Titans were better for more of those years',
#           "Titans got a year of Jason Babin's brief peak"],
#     'LB': ['Mr.Monday Night!','Godfrey was really good in the early NFL 2K games',
#            'Fokou, Marshall AV per game may be inflated by few games played',
#            'Not a lot of recent LBs with long careers here'],    
#     'WR': ['AJ Brown in 2022 and beyond would be nice',
#            "don't remember Drew Hill and Ernest Givins",'Titans are not a WR team'],
#     'CB': ["don't remember Cris Dishman", 'similar to LB, not long careers of recent; Jason McCourty left after 2016',
#            "Samari Rolle was good!", "did Pacman's returns contribute to his AV?"],
#     'S': ['Kevin Byard on his way to the top','Blaine Bishop was good',
#           "Titan's trajectory over Michael Griffin's career was sad"],
#     'TE': ['Walker and Wycheck are legends',
#            'Titans have had a few TEs with steady production over a lot of years'],
#     'ST': ['RIP Rob Bironas', 'will Stonehouse join legends, Hentrich and Kern?',
#            'Kickers, Punters, and Longsnappers should be considered separately, but were combined due to low numbers']
#     }
# p = Path(Path.cwd(), 'tables', 'Titans_AV_analysis_90s.json')
# with open(p, 'w', encoding='utf-8') as file:
#     file.write(json.dumps(AV_analysis))     
# del AV_analysis

    
#     # Analysis for graphs with "Titans Era", 6 games played cutoff
# AV_analysis = {
#     'OL':['Bruce Matthews had an awesome career',
#           'Taylor Lewan not labelled, he is right beside David Stewart',
#           'Lewan and Ben Jones are only current Titans with over 100 games played',
#           'Titans enjoyed some long, productive OL careers early on'],
#     'QB':['RIP Steve McNair','Interesting that Tannehill and Mariota show similar rate to McNair (and Moon).',
#           'Titans legend, Ryan Fitzpatrick!'],
#     'DT':["don't remember Henry Ford well",'Jeffery Simmons will be a legend in time, to no suprise',
#           'DaQuan Jones spent a longer time here than I thought'],
#     'RB':['Titans have had some elite RBs','CJ2K and Eddie George are legends',
#           'Henry has lower AV per game due to low usage in his early years',          
#           'DeMarco Murray was most of the Titans offense for a time'],
#     'DE':['Exterior DL / EDGE, with a number of names moved from LB',
#           'Jurrell Casey was so good for so long! If only Titans were better for more of those years',
#           'Harold Landry narrowly missed labelling, he is by Carter/Orakpo'],
#     'LB': ['Mr.Monday Night!','Godfrey was really good in the early NFL 2K games',
#            'Jayon Brown is to right of Evans/Thornton, within shaeded area',
#            'Not a lot of recent LBs with long careers here'],  
#     'WR': ['AJ Brown in 2022 and beyond would be nice. His production rate is extreme relative to Titans WRs',
#            'Titans are not and have not been a WR team', 
#            'Nate Washington most recent long-time contributor'],
#     'CB': [ "Samari Rolle was good!","did Pacman's returns contribute to his AV?",
#            'similar to LB, not long careers of recent; Jason McCourty left after 2016'],           
#     'S': ['Kevin Byard is on his way to the top','Blaine Bishop was good',
#           "Titan's trajectory over Michael Griffin's career was sad",
#           'Some valuable short time contributors, and some long time legends'],
#     'TE': ['Walker and Wycheck are legends',
#            "Jonnu Smith, Anthony Firkser just under Jared Cook. Smith's production suffered an increased blocking role with poor Tackle play.",
#            'Titans have had a few TEs with steady production over a lot of years'],
#     'ST': ['Positional grouping broken apart as positional value is not similar',
#            'RIP Rob Bironas', 'will Stonehouse join legends, Hentrich and Kern?',
#            ]
#     }

# p = Path(Path.cwd(), 'tables', 'Titans_AV_analysis_Titans.json')
# with open(p, 'w', encoding='utf-8') as file:
#     file.write(json.dumps(AV_analysis))     
# del AV_analysis

    
    # Graphs
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patheffects as path_effects

for analyze_position in sub.Pos2.unique():
    graph_data = sub[sub.Pos2==analyze_position]
    pos_list = f'Position List: {", ".join(list(graph_data.Pos.unique()))}'
    
    sns.regplot(data=graph_data, y='AV', x='G', scatter=False,
                line_kws={'alpha':0.2, 'color':'tan', 'lw':2})
    sns.scatterplot(data=graph_data, y='AV', x='G', size=graph_data.G, size_norm=(sub.G.min(),graph_data.G.max()),
                  hue='AV/G',  palette='bone_r', legend=False, edgecolor='#bababa')
    plt.axis([graph_data.G.min()-graph_data.G.max()*.05, graph_data.G.max()+graph_data.G.max()*.05, 0 ,graph_data.AV.max()+graph_data.AV.max()*.05])
    plt.ylabel('Total AV with Titans', fontsize='large',fontweight='bold')
    plt.xlabel('Games played with Titans', fontsize='large',fontweight='bold')
    plt.suptitle(f"Titans AV for {analyze_position}'s", x=0.26, y=0.87)
    plt.title(pos_list,loc='left',fontsize='x-small', y = 0.99)

    n_labels = 5 #if graph_data.shape[0] > 20 else 4
    y_txt = graph_data.AV.max()*0.01
    named = pd.DataFrame(columns = graph_data.columns)

    for col in ['G','AV','AV/G']:
        # top = graph_data.sort_values(col,ascending=False)[0:n_labels]

        if col == 'AV/G' and graph_data.shape[0] > 20:
            top = graph_data[(graph_data.G>=np.floor(np.percentile(graph_data.G,25)))].sort_values(col,ascending=False)[0:n_labels]
        else:
            top = graph_data.sort_values(col,ascending=False)[0:n_labels]

        for val in top.index:
            if val not in named.index:
                check =  abs(top.loc[val,['G','AV']] - named.loc[:,['G','AV']])
                # check['spread'] = check.G+check.AV
                # check = check[check.spread < 20]
                # if check.spread.min() < 20:  
                check = check[(check.G<20) & (check.AV < 5)]
                if check.shape[0] % 2 == 1:
                    plt.annotate(f'{top.loc[val,"Player"]}', (top.loc[val,'G']+1, top.loc[val,'AV']-y_txt),
                                fontsize='small', ha='left', va='top',
                                  arrowprops={'arrowstyle':"->",'connectionstyle':'arc',}
                                )
                else:
                    plt.annotate(f'{top.loc[val,"Player"]}', (top.loc[val,'G']-1, top.loc[val,'AV']+y_txt),
                                fontsize='small', ha='right', va='bottom',
                                #arrowprops={'arrowstyle':"->",'connectionstyle':'arc',}
                                )
                named.loc[val,:] = top.loc[val,:]

    plt.savefig(f'Titans AV graphs/90s_{analyze_position}_AV2.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('plot created for', analyze_position)
        
    # Special Graph for Special Teams
analyze_position = 'ST'
graph_data = sub[sub.Pos2==analyze_position]
pos_list = f"Position List: {', '.join(list(graph_data.Pos.unique()))}"

palette_list = ['Reds','Blues','Greens']
reg_list = ['salmon','lightblue','lightgreen']

for i, pos in enumerate(graph_data.Pos.unique()):
    sns.regplot(data=graph_data[graph_data.Pos == pos], y='AV', x='G', scatter=False, # truncate=True,
                line_kws={'alpha':0.2, 'color':reg_list[i], 'lw':2})
    sns.scatterplot(data=graph_data[graph_data.Pos == pos], y='AV', x='G', size='G', size_norm=(sub.G.min(),graph_data.G.max()),
                  hue='AV/G', hue_norm=(graph_data['AV/G'].min(),graph_data['AV/G'].max()),
                  palette=palette_list[i], legend=False, edgecolor='#bababa')

plt.axis([graph_data.G.min()-graph_data.G.max()*.05, graph_data.G.max()+graph_data.G.max()*.05, 0 ,graph_data.AV.max()+graph_data.AV.max()*.05])
plt.ylabel('Total AV with Titans', fontsize='large',fontweight='bold')
plt.xlabel('Games played with Titans', fontsize='large',fontweight='bold')
plt.suptitle(f"Titans AV for {analyze_position}'s", y=0.87, x=0.26)
plt.title(pos_list,loc='left',fontsize='x-small', y = 0.99)

pos_pos = {'K':['Kickers',(0.3,0.6)],'P':['Punters',(0.88,0.57)], 'LS':['Long Snappers',(0.65,0.05)]}
# position labels
for i,pos in enumerate(graph_data.Pos.unique()):
      plt.text(pos_pos[pos][1][0]*graph_data.G.max(),pos_pos[pos][1][1]*graph_data.AV.max(),
                pos_pos[pos][0], color=reg_list[i], ha='left', fontweight='bold', fontsize='large', 
              path_effects=[path_effects.Stroke(linewidth=0.5, foreground='black')])


n_labels = 5
y_txt = graph_data.AV.max()*0.01
named = pd.DataFrame(columns = graph_data.columns)

for col in ['G','AV','AV/G']:
    top = graph_data.sort_values(col,ascending=False)[0:n_labels]
    for val in top.index:
        if val not in named.index:
            check =  abs(top.loc[val,['G','AV']] - named.loc[:,['G','AV']]) 
            check = check[(check.G<20) & (check.AV < 5)]
            if check.shape[0] % 2 == 1:
                plt.annotate(f'{top.loc[val,"Player"]}', (top.loc[val,'G']+1, top.loc[val,'AV']-y_txt),
                            fontsize='small', ha='left', va='top',
                              arrowprops={'arrowstyle':"->",'connectionstyle':'arc',}
                            )
            else:
                plt.annotate(f'{top.loc[val,"Player"]}', (top.loc[val,'G']-1, top.loc[val,'AV']+y_txt),
                            fontsize='small', ha='right', va='bottom')
            named.loc[val,:] = top.loc[val,:]

plt.savefig(f'Titans AV graphs/Titans_{analyze_position}_AV.png', dpi=300, bbox_inches='tight')
plt.close()
print('plot created for', analyze_position)


    