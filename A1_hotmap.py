# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 10:00:57 2021

@author: Liang
"""


import folium
from folium.plugins import HeatMap
import numpy as np
import pandas as pd
import re
import requests

#設定地圖中心點
def Creat_map(County, Kind):
    
    m = folium.Map(location=[23.90272076995964, 120.69050876684112], zoom_start=17)
    Data_fn = '{}.json'.format(Kind)
    
   
    All_datas = pd.read_json(Data_fn)
    heat_df = list()
    
    for Each_data in All_datas.iloc[1,1]:
        if County != "":
            if (re.search(County, Each_data['發生地點'])):
                heat_df.append([float(Each_data['緯度']), float( Each_data['經度'])])
        else:
            heat_df.append([float(Each_data['緯度']), float( Each_data['經度'])])
    
    
    heat_data =[row for row in heat_df]
    
    
    HeatMap(data = heat_data).add_to(m)
    #存在地圖檔
    m.save(r'Map\{}_heatmap.html'.format(Kind))
    
    
    
    
if __name__ == '__main__':
    County_name = "南投縣"
    Kind = 'A1'
    Creat_map(County_name, Kind)