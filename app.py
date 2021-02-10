import folium
import pandas as pd

volcanoMap = pd.read_csv("Volcanoes.txt")
lat = list(volcanoMap['LAT'])
lon = list(volcanoMap['LON'])
elev = list(volcanoMap['ELEV'])
name = list(volcanoMap['NAME'])
loc = list(volcanoMap['LOCATION'])

html = """ <h3 style="font-family:arial;"> Volcano information: </h3> 
<p style="font-family:arial; font-size: 11px"><b>Name:</b> {} </p>
<p style="font-family:arial; font-size: 11px"><b>Location:</b> {} </p>
<p style="font-family:arial; font-size: 11px"><b>Elevation:</b> {} m </p>
"""

def popup_colorer(elevation):
    if elevation < 2000:
        return 'green'
    elif 2000<= elevation < 3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location = [40.6299019,-120.8310013], zoom_start=6, tiles = "Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el, nm, lc in zip(lat, lon, elev, name, loc):
    iframe = folium.IFrame( html = html.format(nm, lc, str(el)), width = 220, height = 120)
    fgv.add_child(folium.CircleMarker(location=[lt, ln],radius=6, popup=folium.Popup(iframe),
    fill_color=popup_colorer(el), color ='grey', fill_opacity=0.7))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 20000000
else 'orange' if 20000000 <= x['properties']['POP2005']< 100000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)

map.add_child(folium.LayerControl())

map.save("Map1.html")
