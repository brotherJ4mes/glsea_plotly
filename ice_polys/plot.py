#!/bin/python3.11

import geopandas as gpd
import pandas as pd
#import geodatasets
import folium
import matplotlib.pyplot as plt


gdf = gpd.read_file('GL260218_lam.shp')

df = pd.DataFrame({'CT': pd.to_numeric(gdf['CT']), 'SA': pd.to_numeric(gdf['SA'])})
df.loc[df['CT'] == 91,'CT'] = 95
df.loc[df['CT'] == 92,'CT'] = 100
df.loc[df['CT'] == 00,'CT'] = pd.NA # OMIT 0%


#df2 = gpd.read_file('GL260218.kmz')

m = folium.Map([46, -84], tiles='CartoDB dark_matter', zoom_start=6)
folium.Choropleth(
    geo_data=gdf,
    data=df['CT'],
    #columns=['CT', 'SA'],
    columns=['CT'],
    key_on='feature.id',
    fill_color='YlOrRd',
    nan_fill_opacity = 0,
    line_weight=0.5,
).add_to(m)


m.show_in_browser()



