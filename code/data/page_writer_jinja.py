from pathlib import Path
import json
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment( 
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

# date modified of 2022 pbp data
p = Path(Path.cwd(), 'pbp data','play_by_play_2022.parquet')
date = pd.Timestamp.fromtimestamp(p.stat().st_mtime).strftime('%c') # through reg season

# puntalytics date, check last game_id
adv_date = pd.Timestamp(year=2023, month=12, day = 30).strftime('%x') # week 17 after TNF
#print(adv_date, type(adv_date))


# HTML tables and whatever dictionaries
p = Path(Path.cwd(),'tables')

# Career AV tables, notes of for each graph
with open(Path(p,'Titans_AV_tables_Titans.json'), 'r') as file:
    AV_tables = json.loads(file.read())
with open(Path(p,'Titans_AV_analysis_Titans.json'), 'r') as file:
    AV_analysis = json.loads(file.read())

# punter tables
with open(Path(p,'punting_tables.json'), 'r') as file:
    punting_tables = json.loads(file.read())  

# Punters are Players, play descriptions
if Path(Path.cwd(),'processed data','punter_other_desc_2022.json').exists():
    with open(Path(Path.cwd(),'processed data','punter_other_desc_2022.json'), 'r') as file:
        p_also = json.loads(file.read()) 
else:
    p_also = None        
if Path(Path.cwd(),'processed data','punter_other_desc_Titans.json').exists():
    with open(Path(Path.cwd(),'processed data','punter_other_desc_Titans.json'), 'r') as file:
        p_also2 = json.loads(file.read()) 
else:
    p_also2 = None 
 

# write to public template and save
template = env.get_template('template_public.html')
with open(Path(Path.cwd().parent,'TitanUp - public repo','docs','index.html'), 'w', encoding='utf-8') as page:
    page.write(template.render(date=date, AV_tables=AV_tables, AV_analysis=AV_analysis, adv_date=adv_date,
        punting_tables=punting_tables, p_also=p_also, p_also2=p_also2,
                              ))   

# write to template and save
template = env.get_template('template_public.html')
with open('page_punters.html', 'w', encoding='utf-8') as page:
    page.write(template.render(date=date, AV_tables=AV_tables, AV_analysis=AV_analysis,
        punting_tables=punting_tables, p_also=p_also, p_also2=p_also2, adv_date=adv_date,
                               ))   