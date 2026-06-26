#!/usr/bin/python3.11
import json
import geopandas as gpd
import pandas as pd
import numpy as np
#import plotly.graph_objects as go
import plotly.express as px

#   - [ ] go back to KMZ (already spherical, cleaner)
#   - [ ] fix name issue
#   - [ ] fix coordinate issue


# 1. Load the shapefile
# Geopandas can read directly from a zip file using the 'zip://' prefix
shapefile_path = "zip://GL260218_lam.zip"
#shapefile_path = "GL260218.kmz"

# Alternatively, if you have already extracted the files locally, use:
# shapefile_path = "GL260218_lam.shp"

print("Loading shapefile...")
gdf = gpd.read_file(shapefile_path)


# 3. Reproject to WGS84 (EPSG:4326) as required by Plotly maps
print("Reprojecting coordinates to WGS84...")
gdf = gdf.to_crs(epsg=4326)

# Create a unique string identifier per row to match with GeoJSON
gdf['id'] = gdf.index.astype(str)
geodat = json.loads(gdf.geometry.to_json())


ct_dict = {        
#ct_dict = {"00":"0", 
           "20":"20",
           "30":"30",
           "50":"50",
           "60":"60",
           "70":"70",
           "80":"80",
           "90":"90",
           "91":"95",
           "92":"100",
           }


sa_dict_mm = {"0":0, 
            "81":10,
            "84":50,
            "85":150,
            "87":300,
            "91":700,
           }

fa_dict = {
    '01': 'small ice cake, brash ice',
    '03': 'small floe',
    '04': 'medium floe',
    '05': 'big floe',
    '06': 'vast floe',
    '07': 'giant floe',
    '08': 'landfast',
    }




mako_palette = ["#0B0405", "#28192F", "#3B2F5E", "#40498E", "#366A9F", "#348AA6", "#38AAAC", "#54C9AD", "#A0DFB9", "#DEF5E5"]

ice = pd.DataFrame(gdf.drop(columns='geometry'))
ice['cover'] = ice['CT'].map(ct_dict)
ice['thickness'] = ice['SA'].map(sa_dict_mm)
ice['form'] = ice['FA'].map(fa_dict)


#https://plotly.com/python/tile-county-choropleth/
fig = px.choropleth_map(
    ice, geojson=geodat, locations='id', color='cover',
                           color_discrete_sequence=mako_palette,
    custom_data=['cover','thickness','form'],
    #center={"lat": center_lat, "lon": center_lon},
    map_style="light"
)


hover_temp = 'cover: %{customdata[0]}% <br> thickness: %{customdata[1]} mm <br> form: %{customdata[2]}'
fig.update_traces(hovertemplate=hover_temp)
#fig.update_traces({'name': ''})
print("Generating map layers...")

fig.update_layout(
    map=dict(
        center={'lat': 45.0, 'lon': -84.0},
        zoom=6),
    )

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


fig.update_layout(
        updatemenus=[
        dict(
            buttons=map_sty_buttons,
            type='dropdown',
            direction='down',
            pad={"r": 10, "t": 10},
            x=1.0,
            xanchor="right",
            y=1.00,
            yanchor="top"
            )
        ]
    )



fig.write_html('ice_choro.html')



# Render map in browser
#main_fig.show()
