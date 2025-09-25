#!/bin/python3.9
import pandas as pd
import plotly.graph_objects as go
import datetime as dt
import numpy as np
import sys
import calendar
from PIL import Image



# ==== settings =====
#lk = 'sup' # see lkname dictionary for all
lk = sys.argv[1]
main_font = 18
leg_font  = 14
cred_font = 18
# ==================


lkname = dict(sup='Superior', mic='Michigan', hur='Huron', eri='Erie', ont='Ontario')
print(f'{lkname[lk]}...')
#short_lk = dict(s='sup', m='mic', h='hur', e='eri', o='ont') # just for saving output file

lst = pd.read_table('https://apps.glerl.noaa.gov/coastwatch/webdata/statistic/csv/all_year_glsea_avg_'+lk[0]+'_C.csv', sep=',')
lst = lst.drop(lst.columns[0], axis=1)
yrs = lst.columns.astype('int').values # define years based on column headers


## opt: shift leap years
#not_ly = [ not(calendar.isleap(y)) for y in lst.columns.values.astype('int') ]
#lst.iloc[60:,not_ly] = lst.iloc[59:-1, not_ly]
#lst.iloc[59, not_ly] = np.nan
# dts = pd.date_range('2000-01-01', '2000-12-31')#.strftime('%b-%d') # use a NON leap year for omitting

# opt: omit leap years
ly = [ calendar.isleap(y) for y in lst.columns.values.astype('int') ]
lst.iloc[59:-1,ly] = lst.iloc[60:, ly]
lst = lst.drop(365,axis=0)
dts = pd.date_range('2001-01-01', '2001-12-31')#.strftime('%b-%d') # use a NON leap year for omitting

# handle dts
lst.index = dts


# add average, convert to F and round
lst.insert(lst.shape[1], 'average', lst.mean(1, numeric_only=True)) # insert average at end
#lst = lst.round(decimals=1)
lst_F = lst*9/5 + 32
#lst_F = lst_F.round(decimals=1)


deg_C = np.repeat('°C',366)
deg_F = np.repeat('°F',366)


fig = go.Figure()
[ fig.add_traces(go.Scatter(x=lst.index, y=lst[col], name=col, customdata=deg_C)) for col in lst.columns ]
fig.update_traces(line_color='lightblue')
fig.update_traces(selector=dict(name='2025'), line_color='blue')
fig.update_traces(selector=dict(name='average'), line_color='black')
fig.update_layout(
                 yaxis=dict(title=dict(text='lake-wide surface temperature')),
                 plot_bgcolor='white',
                 font=dict(size=main_font),
                 legend=dict(font=dict(size=leg_font)),
                 title=dict(text=f'Lake {lkname[lk]} GLSEA', x=0.5, xanchor='center'),
                 )


#for fig_scatter_data in fig.data:
#    fig_scatter_data['customdata'] = [fig_scatter_data['name']] * len(fig_scatter_data['x'])



fig.update_traces(
    hovertemplate = 
    #"%{x}, %{customdata} <br>" + 
    "<b>%{y:.1f} %{customdata}</b>, %{x|%b-%d}"
    )

list_traces_F = [ lst[col]*9/5+32 for col in lst.columns ]
list_traces_C = [ lst[col]for col in lst.columns ]

rand_colors =['aqua', 'aquamarine', 'bisque', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'rebeccapurple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow']


# fig.update_traces(selector=dict(name='2025'), line_color='blue', selected_marker_color='red')
#fig.update_traces(selector=dict(name='2021'), line_color='red')
#dict(method='restyle', label='1995', args=[{'line.color': 'blue'}, [0]], args2=[{'line.color': 'lightblue'}, [0]]),

# yrs is defined based on the LST read in but can manually override it below for testing
#yrs = np.arange(1995,2000)
#yrs = np.arange(1995,2010) 
ii = np.arange(len(fig.data)) # total num traces
rand_colors = np.append(rand_colors[:len(yrs)], 'black') # shorten rand_colors and add black for mean


# to change a trace color(s) you can use args=[{'line.color', 'red'}, [1,2,4,5] ] which is useful
# (especially for the "None" option where I want to remove highlighting but preserve black avg)
# however this doesn't work for dynamically changing which SINGLE year is hilighted
# instead i'll generate lists using args=[{'line.color', ['blue','lightblue,'lightblue,'lightblue',....]}]
# so that each new year selection will unselect previous years that were hilighted

def gen_color_list(year):
    return(np.append(np.where(yrs==year, 'blue','lightblue'),'black').tolist())

hilit_button = list([dict(method='restyle', label=str(y), args=[{'line.color': gen_color_list(y)}]) for y in yrs ])
hilit_button.insert(0, dict(method='restyle', label='None', args=[{'line.color': 'lightblue'}, ii[:-1]]))
hilit_button.append(dict(method='restyle', label='All Unique', args=[ {'line.color': rand_colors }]))

# The below allows cumulative highlighting
#hilit_button = list([dict(method='restyle', label=str(y), args=[{'line.color': 'blue'}, [i]]) for i,y in enumerate(yrs) ])
#hilit_button.insert(0, dict(method='restyle', label='None', args=[{'line.color': 'lightblue'}, ii[:-1]]))
# hilit_button.append(dict(method='restyle', label='All Unique', args=[ {'line.color': rand_colors }]))





def gen_color_list(year):
    return(np.append(np.where(yrs==year, 'blue','lightblue'),'black').tolist())

hilit_button = list([dict(method='restyle', label=str(y), args=[{'line.color': gen_color_list(y)}]) for y in yrs ])
hilit_button.insert(0, dict(method='restyle', label='None', args=[{'line.color': 'lightblue'}, ii[:-1]]))
hilit_button.append(dict(method='restyle', label='All Unique', args=[ {'line.color': rand_colors }]))



fig.update_xaxes(dtick='M1', tickformat='%b')

unit_buttons = list([
    dict(method= 'update',
        label='Fahrenheit',
        args=[
            { 'y': list_traces_F,
             'customdata': [ deg_F ],
            # 'yaxis': dict(title=dict(text='lake surface temperature (°F)'))
              }
        ]),
    dict(method= 'update',
        label='Celsius',
        args=[
            { 'y': list_traces_C,
             'customdata': [ deg_C ],
            # 'yaxis': dict(title=dict(text='lake surface temperature (°F)'))
              }
        ]),
])


fig.update_layout(
        updatemenus=[
            dict(
            buttons=unit_buttons,
            type='buttons',
            direction='down',                       
            active=1,
            pad={"r":0, "t": 0},
            x=1.0,
            xanchor="right",
            y=.975,
            yanchor="top"
            ),
            dict(
            buttons=hilit_button,
            type='dropdown',
            #pad={"r":-1, "t": -1, "b": -1, "l": -1},
            direction='down',
            active=len(yrs),
            x=1.0,
            xanchor="right",
            y=.85,
            yanchor="top"
            )
            ]
        )



fig.add_annotation(
                   text = 'NOAA CoastWatch <br>Great Lakes Environmental Research Lab ',
                   xref='paper',
                   yref='paper',
                   x=0.05, 
                   y=1.00,
                   xanchor="left",
                   yanchor="top",
                   showarrow=True,
                   align='left',
                   #font=dict(size=24, color='white'),
                   font=dict(size=cred_font),
                   #borderpad=6,
                   )

NOAA_logo = Image.open('/home/kessler/plot_gen/map_glsea/noaa-logo-rgb-2022.png')

fig.add_layout_image(
    dict(
        #source="noaa-logo-rgb-2022.png",
        #source="https://space.commerce.gov/wp-content/uploads/noaa-logo-rgb-2022.png",
        source=NOAA_logo,
        xref="paper",
        yref="paper",
        x=.05,
        y=.96,
        sizex=.07,
        sizey=.07,
        sizing="contain",
        opacity=1,
        layer="above"
    )
)



fig.write_html(f'html/out_spag_{lk}.html')
fig.write_json(f'out_spag_{lk}.json')






