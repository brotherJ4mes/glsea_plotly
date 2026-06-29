#!/bin/python3.9
import pandas as pd
#import plotly.graph_objects as go
import plotly.express as px
import datetime as dt
import numpy as np
import sys
import calendar
from PIL import Image



# ==== settings =====
lk = 'bas' # see lkname dictionary for all
#lk = sys.argv[1]
main_font = 18
leg_font  = 14
cur_year = '2026'
cred_font = 18
# ==================


lkname = dict(sup='Lake Superior', mic='Lake Michigan', hur='Lake Huron', eri='Lake Erie', ont='Lake Ontario', bas='Great Lakes')
print(f'{lkname[lk]}...')
#short_lk = dict(s='sup', m='mic', h='hur', e='eri', o='ont') # just for saving output file

base_dir = 'https://www.glerl.noaa.gov/data/ice/glicd/daily/'
ice = pd.read_table(f'{base_dir}/{lk}.txt', header=0, sep='\s+')
ice = ice.drop(ice.columns[0], axis=1)
yrs = ice.columns.astype('int').values # define years based on column headers


## opt: shift leap years
#not_ly = [ not(calendar.isleap(y)) for y in lst.columns.values.astype('int') ]
#lst.iloc[60:,not_ly] = lst.iloc[59:-1, not_ly]
#lst.iloc[59, not_ly] = np.nan
# dts = pd.date_range('2000-01-01', '2000-12-31')#.strftime('%b-%d') # use a NON leap year for omitting

# opt: omit leap years
ly = [ calendar.isleap(y) for y in ice.columns.values.astype('int') ]
ice = ice.drop('Feb-29')
dts = pd.date_range(start=ice.index[0]+'-2000', end=ice.index[-1]+'-2001')

# handle dts
ice.index = dts


# add average, convert to F and round
ice.insert(ice.shape[1], 'average', ice.mean(1, numeric_only=True)) # insert average at end

ice = ice.round(decimals=1)


fig = px.line(ice, x=ice.index, y=ice.columns)
fig.update_traces(line_color='lightblue', line_width=2.0)
fig.update_traces(selector=dict(name=cur_year), line_color='blue', line_width=2.0)
fig.update_traces(selector=dict(name='average'), line_color='black', line_width=2.0)


fig.update_layout(
                 yaxis=dict(title=dict(text='lake-wide ice cover')),
                 xaxis=dict(title=dict(text='')),
                 plot_bgcolor='white',
                 font=dict(size=main_font),
                 legend=dict(font=dict(size=leg_font)),
                 title=dict(text=f'{lkname[lk]}', x=0.5, xanchor='center'),
                 )

fig.update_xaxes(dtick='M1', tickformat='%b')
fig.update_yaxes(range=[0,100])
fig.update_traces(
    hovertemplate = 
    #"%{x}, %{customdata} <br>" + 
    "<b>%{y:.1f}%</b>,  %{x|%b-%d}",
    showlegend=False
    )
## to change a trace color(s) you can use args=[{'line.color', 'red'}, [1,2,4,5] ] which is useful
## (especially for the "None" option where I want to remove highlighting but preserve black avg)
## however this doesn't work for dynamically changing which SINGLE year is hilighted
## instead i'll generate lists using args=[{'line.color', ['blue','lightblue,'lightblue,'lightblue',....]}]
## so that each new year selection will unselect previous years that were hilighted
#
def gen_color_list(year):
    return(np.append(np.where(yrs==year, 'blue','lightblue'),'black').tolist())
#
## The below allows cumulative highlighting
##hilit_button = list([dict(method='restyle', label=str(y), args=[{'line.color': 'blue'}, [i]]) for i,y in enumerate(yrs) ])
##hilit_button.insert(0, dict(method='restyle', label='None', args=[{'line.color': 'lightblue'}, ii[:-1]]))
## hilit_button.append(dict(method='restyle', label='All Unique', args=[ {'line.color': rand_colors }]))

def gen_color_list(year):
    return(np.append(np.where(yrs==year, 'blue','lightblue'),'black').tolist())

ii = np.arange(len(fig.data)) # total num traces
hilit_button = list([dict(method='restyle', label=str(y), args=[{'line.color': gen_color_list(y)}]) for y in yrs ])
hilit_button.insert(0, dict(method='restyle', label='None', args=[{'line.color': 'lightblue'}, ii[:-1]]))

#crds_button = list([
#        dict(
#        args=['hovertemplate', '<b>%{z:.1f}</b> <br>%{customdata[0]:.2f}°N<br>%{customdata[1]:.2f}°W'],
#        args2=['hovertemplate',  '<b>%{z:.1f}</b>'],
#        label='show coordinates',
#        method='restyle'
#        )
#        ])


showleg_button = list([
        dict(
        method='update', 
        label='show legend', 
        args=[{'showlegend': True}], 
        args2=[{'showlegend': False, 'visible': True}]
        ) 
        ])

#hilit_button.append(dict(method='restyle', label='All Unique', args=[ {'line.color': rand_colors }]))
fig.update_layout(
        updatemenus=[
            dict(
            buttons=showleg_button,
            type='buttons',
            active=1,
            pad={"r": 10, "t": 10},
            x=0.9,
            xanchor="right",
            y=1.0,
            yanchor="top"
            ),
            dict(
            buttons=hilit_button,
            type='dropdown',
            pad={"r": 10, "t": 10},
            #pad={"r":-1, "t": -1, "b": -1, "l": -1},
            direction='down',
            active=len(yrs),
            x=0.9,
            xanchor="right",
            y=.92,
            yanchor="top"
            )
            ]
        )


fig.write_html('ice_spag.html')
#
#
#fig.add_annotation(
#                   text = 'NOAA CoastWatch <br>Great Lakes Environmental Research Lab ',
#                   xref='paper',
#                   yref='paper',
#                   x=0.05, 
#                   y=1.00,
#                   xanchor="left",
#                   yanchor="top",
#                   showarrow=True,
#                   align='left',
#                   #font=dict(size=24, color='white'),
#                   font=dict(size=cred_font),
#                   #borderpad=6,
#                   )
#
#NOAA_logo = Image.open('/home/kessler/plot_gen/map_glsea/noaa-logo-rgb-2022.png')
#
#fig.add_layout_image(
#    dict(
#        #source="noaa-logo-rgb-2022.png",
#        #source="https://space.commerce.gov/wp-content/uploads/noaa-logo-rgb-2022.png",
#        source=NOAA_logo,
#        xref="paper",
#        yref="paper",
#        x=.05,
#        y=.96,
#        sizex=.07,
#        sizey=.07,
#        sizing="contain",
#        opacity=1,
#        layer="above"
#    )
#)
#
#
#
#fig.write_html(f'html/out_spag_{lk}.html')
fig.write_json(f'out_spag_{lk}.json')
#
#
#
#
#
#
