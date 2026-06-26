import pandas
import folium
import requests

m = folium.Map([43, -100], zoom_start=4)

us_states = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
).json()

state_data = pandas.read_csv(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_unemployment_oct_2012.csv"
)


folium.Choropleth(
    geo_data=us_states,
    data=state_data,
    columns=["State", "Unemployment"],
    key_on="feature.id",
).add_to(m)

m

m.show_in_browser()
