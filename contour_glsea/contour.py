#!/bin/python3.9
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import sys
from datetime import datetime


base_dir = '/mnt/cwdata/p/m/lcd/'
yyyy     = sys.argv[1]
mm       = sys.argv[2]
jjj      = sys.argv[3]

fin = f'{base_dir}/{yyyy}/{mm}/{yyyy}_{jjj}_glsea.asc'

#[yr, jd] = re.findall('\d+', os.path.basename(fin))
val_date = datetime.strptime(yyyy+'-'+jjj, '%Y-%j')



#lst_gl = np.matrix(pd.read_table('2025_266_glsea.asc', skiprows=6, sep='\s+', header=None))
lst_gl = np.matrix(pd.read_table(fin, skiprows=6, sep='\s+', header=None))
ids = np.matrix(pd.read_table('1024_lake_ids.txt', sep='\s+', header=None)) # a modified vers of ids.txt with Stc=Eri=4
#lst_gl[lst_gl==255.0] = np.nan
#lst_F = lst_C * 9/5 + 32.0
#lst[lst==255.0] = -1


# get coords for lat/lon
with open('lats.txt') as f: lats = [float(line.strip()) for line in f]
with open('lons.txt') as f: lons = [float(line.strip()) for line in f]
lats = np.flip(np.array(lats))
lons = -np.array(lons)


def draw_plt(lst, lons, lon_sel, lats, lat_sel, lk): #{{{
    print(f'plotting {lk}...')

    # mask out other lakes (since a rectangle isnt sufficient for some lakes)
    lst_lk = lst.copy() # duplicate global LST
    mask = ids==lk_id[lk]
    lst_lk[~mask] = np.nan

    # now subset by the lon/lat box
    x0 = np.min(np.where(lons < lon_sel[0]))
    xf = np.max(np.where(lons > lon_sel[1]))
    yf = np.max(np.where(lats > lat_sel[0]))
    y0 = np.min(np.where(lats < lat_sel[1]))
    lats = lats[y0:yf]
    lons = lons[x0:xf]
    lst_C = lst_lk[y0:yf, x0:xf]
    lst_F = lst_C * 9/5 + 32


    # draw plot
    fig = go.Figure(
        data = go.Contour(
            x=lons, y=lats, z = lst_F, name='',
            hoverongaps=False, colorscale='turbo', connectgaps=False,
            line = dict(color='black'),
            autocontour=True,
            ncontours=20,
            contours=dict(
                showlabels=True,
                labelfont=dict(
                    size=14,
                    color='black'
                    )
                )
            ))

    fig.update_traces(hovertemplate = "%{z:.1f}°F<br>%{y:.2f}N<br>%{x:.2f}W" )
    fig.update_layout(yaxis_scaleanchor="x", yaxis_scaleratio=1.3)
    fig.update_xaxes(range=[max(lons),min(lons)])


#{{{ buttons
    contours_res_button = list([
        dict(
            args=[{"ncontours": 10}],
            label="Few Contours",
            method="restyle"
        ),
        dict(
            args=[{"ncontours": 30}],
            label="Medium Contours",
            method="restyle"
        ),
        dict(
            args=[{"ncontours": 80}],
            label="Many Contours",
            method="restyle"
        ),
        ])

    contours_toggle = list([
        dict(
           args2=[{"contours.showlabels": False,
                   "contours.showlines": False}],
            args=[{"contours.showlabels": True,
                    "contours.showlines": True}],
            label="Show/Hide Contours",
            method="restyle"
        ),
        ])


    unit_buttons = list([
        dict(method= 'update',
            label='Fahrenheit',
            args=[{ 'z': lst_F,
                  "hovertemplate" :'<b>%{z:.1f} °F</b> <br>%{y:.2f} N <br>%{x:.2f} W'
                    }
            ]),
        dict(method= 'update',
           label='Celsius',
            args=[{ 'z': lst_C,
                 "hovertemplate" :'<b>%{z:.1f} °C</b> <br>%{y:.2f} N <br>%{x:.2f} W',
                 } 
           ])
    ])


    fig.update_layout(
            updatemenus=[
            dict(
                buttons=unit_buttons,
                type='buttons',
                active=0,
                direction='left',
                pad={"r": 10, "t": 10},
                x=1.0,
                xanchor="right",
                y=0.96,
                yanchor="top"
                ),
            dict(
                buttons=contours_toggle,
                type='buttons',
                pad={"r": 10, "t": 10},
                x=1.0,
                xanchor="right",
                y=.92,
                yanchor="top"
                ),
            dict(
                buttons=contours_res_button,
                type='dropdown',
                direction='down',
                pad={"r": 10, "t": 10},
                x=1.0,
                xanchor="right",
                y=.88,
                yanchor="top"
                ),
            ])


#}}}


##{{{ begin annotations
#    fig.add_annotation( 
#                   text=val_date.strftime('Valid %b-%d %Y'),
#                   x=1.0, 
#                   y=1.0, 
#                   xanchor="right",
#                   yanchor="top",
#                   showarrow=False,
#                   font=dict(size=24, color='#0085CA'),
#                   #borderpad=6,
#                   )
#
#    fig.add_annotation(
#                   text='NOAA CoastWatch <br> Great Lakes Environmental Research Lab ',
#                   x=1.0, 
#                   y=0.025,
#                   xanchor="right",
#                   yanchor="bottom",
#                   showarrow=False,
#                   font=dict(size=24, color='#0085CA'),
#                   #borderpad=6,
#                   align='right',
#                   )

#}}}

    fig.write_html(f'out_html/{lk}_contour.html', lk)
    fig.write_json(f'out_json/{lk}_contour.json', lk)
#}}}

lk_id = dict(sup=1, mic=2, hur=3, eri=4, ont=5)
draw_plt(lst_gl, lons, [92.40,  84.15],  lats, [46.30,  49.01], 'sup') 
draw_plt(lst_gl, lons, [88.50,  84.75],  lats, [41.50,  46.25], 'mic') 
draw_plt(lst_gl, lons, [84.75,  79.50],  lats, [42.90,  46.35], 'hur') 
draw_plt(lst_gl, lons, [84.00,  78.50],  lats, [41.00,  43.00], 'eri') 
draw_plt(lst_gl, lons, [80.00,  75.75],  lats, [43.00,  44.50], 'ont') 

