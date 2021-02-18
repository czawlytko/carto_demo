import folium
from folium.plugins import MarkerCluster
from folium.plugins import FloatImage
import pandas as pd

# HI Chris! Hi Rohit! Hire me!

loc = 'Pennsylvania Reported Timber Harvest'

title_html = '''
            <html>
            <head>
            <style>
            body {
            font-family: Verdana, sans-serif;
            }
            </style>
            </head>
            <body>
            <h3 align="center" style="font-size:16px"><b>Pennsylvania Reported Timber Harvest</b></h3>

             '''
#            <h4 align="center" style="font-size:12px"><b>{sub}</b></h4>



home_coords = [40.9, -77.3]
my_map = folium.Map(location = home_coords, zoom_start = 8, tiles='Stamen Terrain')
for tiles in ['mapquestopen','MapQuest Open Aerial','Mapbox Control Room']:
    try:
        folium.TileLayer(tiles).add_to(my_map)
    except:
        print(f'could not add {tiles}')
my_map.get_root().html.add_child(folium.Element(title_html))
# my_map.get_root().html.add_child(folium.Element(sub_html))

co_style = lambda x: {'color': '#FF1ACB35'}
counties = folium.GeoJson(r"data/PA_counties.geojson",name="Pennsylvania County Boundaries",style_function=co_style).add_to(my_map)
folium.features.GeoJsonPopup(fields=["NAMELSAD"],labels=False ).add_to(counties)

timber_style = lambda x: {'color': '#1ACB35' if
                            x['properties']['acres']<15 else
                            '#CB391A'}

timb_gjson = folium.GeoJson(r"data\PA_timbersale_labeled.geojson", 
                                name="Timber Harvest Noundaries",
                                zoom_on_click=True, 
                                style_function=timber_style,
                                popup=folium.GeoJsonPopup(fields=['ID','acres'])).add_to(my_map)


url = "data\legend.png"

FloatImage(url, bottom=6, left=6).add_to(my_map)


my_map.add_child(folium.map.LayerControl())

#Display the map
my_map
my_map.save('demo_webmap.html')
print('generated')
