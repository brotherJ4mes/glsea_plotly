#!/bin/python3.9
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import datetime as dt


# ==== settings =====
cur_year = '2025'

main_font = 18
leg_font  = 14
cred_font = 18

# ==================
lkname = dict(s='Superior', m='Michigan', h='Huron', e='Erie', o='Ontario')


def read_lake(lk, unit):
    lst = pd.read_table('https://apps.glerl.noaa.gov/coastwatch/webdata/statistic/csv/all_year_glsea_avg_'+lk+'_C.csv', sep=',')
    lst = lst.drop(lst.columns[0], axis=1)
    dts = pd.date_range('2000-01-01', '2000-12-31')#.strftime('%b-%d')
    lst.index = dts
    out = pd.concat([lst.min(1), lst.mean(1), lst.max(1), lst[cur_year]], axis=1)
    out.columns = ['min','mean','max', cur_year]
    out.insert(0, 'lake', lkname[lk])
    return(out)

#lks_mean = pd.concat([ read_lake_mean(lk,'C') for lk in ('s','m','h','e','o') ], axis=1)
#lks = pd.concat([ read_lake(lk,'C') for lk in ('s','m','h','e','o') ], axis=0)
#lks = pd.concat([ read_lake(lk,'C') for lk in ('s','m','h','e','o') ], axis=0)
sup = read_lake('s','C')
mic = read_lake('m','C')
hur = read_lake('h','C')
eri = read_lake('e','C')
ont = read_lake('o','C')



def hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = hex_color * 2
    return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

deg_C = np.repeat('°C',366)
deg_F = np.repeat('°F',366)


alpha = 0.2
#hovstr='<br>%{x}<br>%{y:.1f}°C'
hovstr='<br>%{x|%b-%d}<br><b>%{y:.1f} %{customdata}</b>'

def add_lake(lk, lkname, col):
    fill_col=f"rgba{(*hex_to_rgb(col), alpha)}"
    # add mean and current year
    fig.add_traces(go.Scatter(x=lk.index, y=lk['mean'], customdata=deg_C, line=dict(color=col, dash='dash', width=3), legendgroup=lkname, legendgrouptitle_text=lkname, name='Mean', hovertemplate=lkname+hovstr))
    fig.add_traces(go.Scatter(x=lk.index, y=lk[cur_year],customdata=deg_C, line=dict(color=col, width=3), legendgroup=lkname, name=cur_year, hovertemplate=lkname+hovstr))
    # add shade envelope
    fig.add_traces(go.Scatter(x=lk.index, y=lk['max'], customdata=deg_C,   line=dict(width=0, color=fill_col), legendgroup=lkname+'_range', name='', visible='legendonly', hovertemplate=lkname+hovstr+'<extra><b>Historical<br>Max</b></extra>'))
    fig.add_traces(go.Scatter(x=lk.index, y=lk['min'],   customdata=deg_C, fill='tonexty', line=dict(width=0, color=fill_col),  fillcolor=fill_col, legendgroup=lkname+'_range', name='Historical Range', visible='legendonly', hovertemplate=lkname+hovstr+'<extra><b>Historical<br>Min</b></extra>'))


# darjeeling1
pal = ("#FF0000", "#00A08A", "#F2AD00", "#F98400", "#5BBCD6")

def c2f(df):
    return(df*9/5 + 32)


fig = go.Figure()
add_lake(sup, 'Superior', pal[0])
add_lake(mic, 'Michigan', pal[1])
add_lake(hur, 'Huron',    pal[2])
add_lake(eri, 'Erie',     pal[3])
add_lake(ont, 'Ontario',  pal[4])


fig.update_xaxes(dtick='M1', tickformat='%b', showspikes=False)
fig.update_layout(
        plot_bgcolor='white', 
        yaxis=dict(title=dict(text='lake-wide surface temperature')),
        font=dict(size=main_font),
        legend=dict(font=dict(size=leg_font))
        )
               

#fig.update_yaxes(range = [0,80])



# begin button craziness
unit_buttons = list([
    dict(method= 'update',
        label='Fahrenheit',
        args=[
            { 'y': [
                c2f(sup['mean']), c2f(sup[cur_year]), c2f(sup['min']), c2f(sup['max']),
                c2f(mic['mean']), c2f(mic[cur_year]), c2f(mic['min']), c2f(mic['max']),
                c2f(hur['mean']), c2f(hur[cur_year]), c2f(hur['min']), c2f(hur['max']),
                c2f(eri['mean']), c2f(eri[cur_year]), c2f(eri['min']), c2f(eri['max']),
                c2f(ont['mean']), c2f(ont[cur_year]), c2f(ont['min']), c2f(ont['max']),
               ],
             'customdata':[
                   deg_F, deg_F, deg_F, deg_F,
                   deg_F, deg_F, deg_F, deg_F,
                   deg_F, deg_F, deg_F, deg_F,
                   deg_F, deg_F, deg_F, deg_F,
                   deg_F, deg_F, deg_F, deg_F,
                   ],
             #'yaxis': dict(title=dict(text='lake surface temperature (°F)'))

              }
            
        ]),
    dict(method= 'update',
       label='Celsius',
       args=[{ 'y': [
                sup['mean'], sup[cur_year], sup['min'], sup['max'],
                mic['mean'], mic[cur_year], mic['min'], mic['max'],
                hur['mean'], hur[cur_year], hur['min'], hur['max'],
                eri['mean'], eri[cur_year], eri['min'], eri['max'],
                ont['mean'], ont[cur_year], ont['min'], ont['max'],
               ],
             'customdata':[
                   deg_C, deg_C, deg_C, deg_C,
                   deg_C, deg_C, deg_C, deg_C,
                   deg_C, deg_C, deg_C, deg_C,
                   deg_C, deg_C, deg_C, deg_C,
                   deg_C, deg_C, deg_C, deg_C,
                   ],
              }
       ])
])


fig.update_layout(
        updatemenus=[
            dict(
            buttons=unit_buttons,
            type='buttons',
            direction='down',
            active=1,
            pad={"r":0, "t": 0},
            showactive=True,
            x=1.0,
            xanchor="right",
            y=.975,
            yanchor="top"
            )
            ]
        )

fig.add_annotation(
                   text='NOAA CoastWatch <br>Great Lakes Environmental Research Lab ',
                   xref='paper',
                   yref='paper',
                   x=0.05, 
                   y=0.85,
                   xanchor="left",
                   yanchor="top",
                   showarrow=True,
                   align='left',
                   #font=dict(size=24, color='white'),
                   font=dict(size=cred_font),
                   #borderpad=6,
                   )

#fig.write_html('html/spag_compare_lks.html')
fig.write_json('spag_compare_lks.json')

