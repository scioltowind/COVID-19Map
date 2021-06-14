# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 14:54:20 2021

@author: Liang
"""
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def Create_Data(url, City_name, Data_Start):
    CDC_Data = pd.DataFrame(pd.read_csv(url))
    MASK1  = CDC_Data['個案研判日'] >= Data_Start
    MASK2 = CDC_Data['縣市'] == City_name
    if City_name =="" or City_name == '全國':
        CDC_Data_2021 = CDC_Data[(MASK1)]
        City_name = '全國'
    else:
        CDC_Data_2021 = CDC_Data[(MASK1 & MASK2)]
    
    Date_Data = CDC_Data_2021.groupby(['個案研判日'])['確定病例數'].sum().reset_index()
    Sex_Data = CDC_Data_2021.groupby(['性別'])['確定病例數'].sum().reset_index()
    Age_Data = CDC_Data_2021.groupby(['年齡層'])['確定病例數'].sum().reset_index()
    Town_Data = CDC_Data_2021.groupby(['鄉鎮'])['確定病例數'].sum().reset_index()

    Draw_plot(Date_Data, Sex_Data, Age_Data, Town_Data, City_name)

def Draw_plot(Date_Data, Sex_Data, Age_Data, Town_Data, City_name):
    
    plt.figure(figsize=(14,14))
    
    #長條圖、折線圖(by 個案研判日)
    plt.subplot(221)
    plt.bar(Date_Data['個案研判日'].astype(str),Date_Data['確定病例數'])
    plt.plot(Date_Data['個案研判日'].astype(str),Date_Data['確定病例數'],'r-^') #畫線
    for x, y in zip(Date_Data['個案研判日'].astype(str), Date_Data['確定病例數'] ):
        plt.text(x, y, y, ha='center',va="bottom",fontsize=14)
    plt.ylim(0, Date_Data['確定病例數'].max()*1.2)
    plt.xticks( rotation ='vertical')
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) 
    plt.title("{}逐日確診數".format(City_name), fontsize = 14)

    #圓餅圖(by 性別)
    plt.subplot(222)
    plt.pie(Sex_Data['確定病例數'], labels = Sex_Data['性別'], autopct='%.2f%%',textprops = {"fontsize" : 14})
    
    plt.title("{}確診數_性別比例".format(City_name), fontsize = 14)


    #長條圖(by 年齡層)    
    plt.subplot(223)
    plt.bar(Age_Data['年齡層'], Age_Data['確定病例數'])
    for x , y in zip(Age_Data['年齡層'], Age_Data['確定病例數']):
        plt.text(x, y, y, ha = 'center', va = 'bottom', fontsize = 14)
    plt.ylim(0, Age_Data['確定病例數'].max()*1.2)
    plt.xticks( rotation ='vertical')
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) 
    plt.title('{}診者年齡分佈'.format(City_name), fontsize = 14)
    
    #長條圖(by 鄉鎮區)    
    plt.subplot(224)
    plt.bar(Town_Data['鄉鎮'], Town_Data['確定病例數'])
    plt.ylim(0, Town_Data['確定病例數'].max()*1.2)
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) 
    for x , y in zip(Town_Data['鄉鎮'], Town_Data['確定病例數']):
        plt.text(x, y, y, ha = 'center', va = 'bottom', fontsize = 14)
    plt.title('{}確診者鄉鎮分佈'.format(City_name), fontsize = 14)
    plt.xticks( rotation ='vertical')
    
    plt.tight_layout()
    plt.savefig("Covid19_statistics.svg", dpi=150)


if __name__  == "__main__":
    url  = 'https://data.cdc.gov.tw/download?resourceid=3c1e263d-16ec-4d70-b56c-21c9e2171fc7&dataurl=https://od.cdc.gov.tw/eic/Day_Confirmation_Age_County_Gender_19CoV.csv'
    City_Name = "南投縣"
    Start_data = 20210501
    Create_Data(url, City_Name, Start_data) 
