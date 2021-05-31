# -*- coding: utf-8 -*-
"""
Created on Thu May 27 14:23:47 2021

@author: Liang


install geopandas
pip install git+git://github.com/geopandas/geopandas.git
"""


import geopandas as gpd
import pandas as pd
import folium
import webbrowser
from folium.features import DivIcon



town_shp = gpd.read_file(r'TOWN_MOI_1100415.shp', encoding = 'utf-8')

Nantou_shp = town_shp[town_shp['COUNTYNAME'] == '南投縣']
Nantou_CNT = pd.read_csv('Counts.csv', encoding = 'utf-8')
Nantou_Data = pd.merge( Nantou_shp,Nantou_CNT , on = 'TOWNNAME')


Nantou_map = folium.Map((23.973694,120.680687),
                        attr='Taiwan Nantou',
                        zoom_start=12)

style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.2, 
                            'weight': 0.1}    

# marker and icon
for i in range(0,len(Nantou_Data)):
    text = Nantou_Data.iloc[i]['TOWNNAME']
    icon = DivIcon(
        icon_size=(150,36),
        icon_anchor=(0,0),
        html='<div style="font-size: 10pt;font-family:DFKai-sb">%s</div>' % text,
        )
    folium.Marker(
        location =[Nantou_Data.iloc[i]['Longitude'], Nantou_Data.iloc[i]['Latitude']],
        icon=icon
    ).add_to(Nantou_map)

                          
folium.Choropleth(
    #傳入geojson
    geo_data=Nantou_Data.to_json(),
    #顏色數據
    data=Nantou_Data,
    #染色區域
    columns=['TOWNNAME',"COUNTS"],
    key_on="feature.properties.TOWNNAME",
    #顏色樣式
    fill_color='OrRd',
    #區域透明度
    fill_opacity=0.5,
    #邊緣透明度
    line_opacity=1,
    line_color='black',
    #圖例名
    legend_name="確診數",
    smooth_factor=0,
    Highlight= True,
    show=False,
).add_to(Nantou_map)

  

NIL = folium.features.GeoJson(
    data = Nantou_Data,
    style_function=style_function, 
    control=False,
    show = True,
    tooltip=folium.features.GeoJsonTooltip(
        fields=['TOWNNAME',"COUNTS"],
        aliases=['鄉鎮名',"確診數"],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)
    
Nantou_map.add_child(NIL)

Nantou_map.save("nantou_map.html")
webbrowser.open_new_tab('nantou_map.html')
