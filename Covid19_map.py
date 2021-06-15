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
import re 

def Data_Process(url ,County_Name):
    
    #導入臺灣省鄉鎮地圖資料
    Town_shp = gpd.read_file(r'mapdata\TOWN_MOI_1100415.shp', encoding = 'utf-8')
    

        
    Nantou_shp = Town_shp[Town_shp['COUNTYNAME'] == County_Name]

    # Nantou_CNT = pd.read_csv('Counts.csv', encoding = 'utf-8')
    # Nantou_Data = pd.merge( Nantou_shp,Nantou_CNT , on = 'TOWNNAME')

    #Read DCD Data and find it about Nantou.
    CDC_Data = pd.read_csv(url)
    CDC_Nantou_Data = CDC_Data[CDC_Data['縣市'] == County_Name]

    #Culcalculate amount about Town, Sex, Age 
    TOWN_Amount = pd.DataFrame(CDC_Nantou_Data.groupby('鄉鎮')['確定病例數'].sum()).reset_index()
    Sex_Amount = pd.DataFrame(CDC_Nantou_Data.groupby(['鄉鎮','性別'])['確定病例數'].sum()).reset_index()
    Age_Amount = pd.DataFrame(CDC_Nantou_Data.groupby(['鄉鎮','年齡層'])['確定病例數'].sum()).reset_index()

    Age_Labels = pd.DataFrame(set(Age_Amount['年齡層'] ), columns = ['年齡層']).sort_values(by = "年齡層")
    TOWN_Amount_Labels = ['鄉鎮','總確診數', '女性確診數', '男性確診數']
    TOWN_Amount_Fields = ['TOWNNAME','總確診數', '女性確診數', '男性確診數']



    # Groupby TownName, Sex
    
    TOWN_Amount = pd.merge(TOWN_Amount, Sex_Amount[Sex_Amount['性別']=='F'][['鄉鎮','確定病例數']], right_on = '鄉鎮', left_on = '鄉鎮', how = 'left')
    TOWN_Amount = pd.merge(TOWN_Amount, Sex_Amount[Sex_Amount['性別']=='M'][['鄉鎮','確定病例數']], right_on = '鄉鎮', left_on = '鄉鎮', how = 'left')
    TOWN_Amount.columns=['鄉鎮','總確診數', '女性確診數', '男性確診數']

    #Groupby  Age and TownName
    for levels in Age_Labels['年齡層']:
        TOWN_Amount = pd.merge(TOWN_Amount, Age_Amount[Age_Amount['年齡層'] == levels][['鄉鎮','確定病例數']], right_on = '鄉鎮', left_on = '鄉鎮', how = 'left')
        TOWN_Amount_Labels.insert(len(TOWN_Amount_Labels), levels)
        TOWN_Amount_Fields.insert(len(TOWN_Amount_Labels), levels)
    TOWN_Amount.columns = TOWN_Amount_Labels


    #NA 補 0 
    TOWN_Amount = TOWN_Amount.fillna(0)


    #Merge map and data
    Nantou_Amount = pd.merge(Nantou_shp,TOWN_Amount , right_on = '鄉鎮', left_on = 'TOWNNAME', how = 'left')
    return (Nantou_Amount, TOWN_Amount_Labels, TOWN_Amount_Fields)



def Create_map(Nantou_Amount, TOWN_Amount_Labels,TOWN_Amount_Fields):
    # Nantou_Amount = data = Nantou_Amount(), columns = ['TOWNNAME', 'Counts'])
    Nantou_map = folium.Map((23.973694,120.680687),
                            attr='Taiwan Nantou',
                            zoom_start=12)
    
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.2, 
                                'weight': 0.1}    
                          
    folium.Choropleth(
        #傳入geojson
        geo_data=Nantou_Amount.to_json(),
        #顏色數據
        data=Nantou_Amount,
        #染色區域
        columns=['TOWNNAME', "總確診數"],
        key_on="feature.properties.TOWNNAME",
        #顏色樣式
        fill_color='YlOrRd',
        #區域透明度
        fill_opacity=0.9,
        #邊緣透明度
        line_opacity=1,
        line_color='black',
        #圖例名
        legend_name="確診數",
        smooth_factor=0,
        Highlight= True,
        nan_fill_color = 'green',
        # bins=10,
        show=False,
    ).add_to(Nantou_map)
    
      
    
    NIL = folium.features.GeoJson(
        data = Nantou_Amount,
        style_function=style_function, 
        control=False,
        show = True,
        # marker  =  foilum.Marker(['TOWNNAME']),
        tooltip=folium.features.GeoJsonTooltip(
            fields = TOWN_Amount_Fields,
            aliases= TOWN_Amount_Labels,
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
        )
    )
        
    Nantou_map.add_child(NIL)
    
    Nantou_map.save("Covid19_map.html")
    webbrowser.open_new_tab('Covid19_map.html')






if __name__ == "__main__":

    County_Name = "南投縣"
    # url  = 'https://data.cdc.gov.tw/download?resourceid=3c1e263d-16ec-4d70-b56c-21c9e2171fc7&dataurl=https://od.cdc.gov.tw/eic/Day_Confirmation_Age_County_Gender_19CoV.csv'
    url ='https://data.cdc.gov.tw/download?resourceid=27ed0b70-c28f-4a44-8a1b-ef13e487ed20&dataurl=https://od.cdc.gov.tw/eic/Age_County_Gender_19Cov.csv'
    Nantou_Amount, TOWN_Amount_Labels,TOWN_Amount_Fields = Data_Process(url, County_Name)
    Create_map(Nantou_Amount, TOWN_Amount_Labels,TOWN_Amount_Fields)
    





