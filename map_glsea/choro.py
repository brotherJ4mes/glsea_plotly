#!/usr/bin/python3.9
import json, sys, re, plotly
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


base_dir = '/mnt/cwdata/p/m/lcd/'
yyyy     = sys.argv[1]
mm       = sys.argv[2]
jjj      = sys.argv[3]

fin = f'{base_dir}/{yyyy}/{mm}/{yyyy}_{jjj}_glsea.dat'


#[yr, jd] = re.findall('\d+', os.path.basename(fin))
val_date = datetime.strptime(yyyy+'-'+jjj, '%Y-%j')


ids = [ str(i).zfill(6) for i in range(148682) ]
with open('cw_polys.geojson') as f:
    geodat = json.load(f)

i=0
for p in geodat['features']:
    p['id'] = ids[i]
    i+=1

lst = pd.read_table(fin, names=['lst_C'])
lst['id'] = ids
lst['lst_F'] = lst['lst_C']*9/5+32

ll = pd.read_table('lat_lon.dat', sep='\s+')
lst = pd.concat([lst, ll], axis=1)
lst['lon'] = -lst['lon']

fig = go.Figure(go.Choroplethmap(geojson=geodat,
                        locations=lst['id'], z=lst['lst_F'],
#                           colorscale="Turbo",
                           colorscale="Turbo",
#                           zmin=32, zmax=86, # if you set these you won't be able to change them via button
                        customdata = np.stack((lst['lat'],lst['lon']), axis=1),
                        name="°F",
                        hoverinfo='z',
                        hovertemplate= '<b>%{z:.1f}</b>',
                        )
                )

fig.update_layout(
    map=dict(
        center={'lat': 45.0, 'lon': -84.0},  
        zoom=6), 
    )

#fig.layout.map.style='satellite'
                            
fig.update_traces(marker_line_width=0)#, customdata= np.stack()

# ============  BEGIN BUTTON DEFINITIONS =================
unit_buttons = list([
    dict(method= 'update',
        label='Fahrenheit',
        args=[ {'z': [lst['lst_F']],
       #       "hovertemplate" :'<b>%{z:.1f} °F</b>',
       #       "zmin":32, 
       #       "zmax":86 ,
              "name":"°F"

                }
        ]),
    dict(method= 'update',
       label='Celsius',
       args=[{ 'z': [lst['lst_C']], 
       #      "hovertemplate" :'<b>%{z:.1f} °C</b>',
       #      "zmin":0, 
       #      "zmax":30,
             "name": "°C"
             } 
       ])
])


cmap_buttons = list([
                dict(
                    args=["colorscale", str(plotly.colors.make_colorscale(plotly.colors.sequential.Turbo)).replace("'", '"')],
                    label="Turbo",
                    method="restyle"
                ),
                dict(
                    args=["colorscale", "Viridis"],
                    label="Viridis",
                    method="restyle"
                ),
                dict(
                    args=["colorscale", str(plotly.colors.make_colorscale(plotly.colors.sequential.Inferno)).replace("'", '"')],
                    label="Inferno",
                    method="restyle"
                ),
                dict(
                    args=["colorscale", "Blackbody"],
                    label="Blackbody",
                    method="restyle"
                ),
                dict(
                    args=["colorscale", "Blues"],
                    label="Blues",
                    method="restyle"
                ),
            ])


# could not get the map style to update, some useful info here:
# https://community.plotly.com/t/python-choropleths-updatemenus/23567
# but this appears to not work under maplibre (mapbox is deprecated so can't test orig soln)
# despite not using mapbox *at all* in this code the json file still contains mapbox: style attributes
# more info here: https://plotly.com/python/mapbox-to-maplibre/
# THE BELOW SOLVED IT: have to reset map frame for some reason
# https://community.plotly.com/t/cannot-relayout-mapbox-style-with-button/82905/2
map_sty_buttons = list([
                dict(
                     args=[{"map": {"style":'light',
                            "center": {"lat": 45.0, "lon": -84.0},
                            "zoom": 6}}],
                    label="light theme",
                    method="relayout"
                ),
                dict(
                     args=[{"map": {"style":'dark',
                            "center": {"lat": 45.0, "lon": -84.0},
                            "zoom": 6}}],
                    label="dark theme",
                    method="relayout"
                ),
                dict(
                     args=[{"map": {"style": 'satellite',
                            "center": {"lat": 45.0, "lon": -84.0},
                            "zoom": 6}}],
                    label="satellite",
                    method="relayout"
                ),
            ])

# map styles
#"basic"
#"carto-darkmatter"
#"carto-darkmatter-nolabels"
#"carto-positron"
#"carto-positron-nolabels"
#"carto-voyager"
#"carto-voyager-nolabels"
#"dark"
#"light"
#"open-street-map"
#"outdoors"
#"satellite"
#"satellite-streets"
#"streets"


crds_button = list([
        dict(
        args=['hovertemplate', '<b>%{z:.1f}</b> <br>%{customdata[0]:.2f}°N<br>%{customdata[1]:.2f}°W'],
        args2=['hovertemplate',  '<b>%{z:.1f}</b>'],
        label='show coordinates',
        method='restyle'
        )
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
            y=.96,
            yanchor="top"
            ),
        dict(
            buttons=crds_button,
            type='buttons',
            active=1,
            pad={"r": 10, "t": 10},
            x=1.0,
            xanchor="right",
            y=0.92,
            yanchor="top"
            ),
        dict(
            buttons=cmap_buttons,
            type='dropdown',
            direction='left',
            pad={"r": 10, "t": 10},
            x=1.0,
            xanchor="right",
            y=0.880,
            yanchor="top"
            ),
        dict(
            buttons=map_sty_buttons,
            type='dropdown',
            direction='left',
            pad={"r": 10, "t": 10},
            x=1.0,
            xanchor="right",
            y=0.84,
            yanchor="top"
            )
        ]
    )


# ============  BEGIN ANNOTATIONS ======================
fig.add_annotation(
                    text=val_date.strftime('Valid %b-%d %Y'),
                   x=1.0, 
                   y=1.0, 
                   xanchor="right",
                   yanchor="top",
                   showarrow=False,
                   font=dict(size=24, color='#0085CA'),
                   borderpad=6,
                   )

fig.add_annotation(
                   text='NOAA CoastWatch <br> Great Lakes Environmental Research Lab ',
                   x=1.0, 
                   y=0.025,
                   xanchor="right",
                   yanchor="bottom",
                   showarrow=False,
                   font=dict(size=24, color='#0085CA'),
                   borderpad=6,
                   align='right',
                   )

fig.add_layout_image(
    dict(
        source="../noaa-logo-rgb-2022.png",
        xref="paper",
        yref="paper",
        x=.9,
        y=.175,
        sizex=.07,
        sizey=.07,
        sizing="contain",
        opacity=1,
        layer="above"
    )
)


fig.write_json('map_choro.json')
fig.write_html('map_choro.html')
