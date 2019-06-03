import numpy as np
import pandas as pd
import sys
import json
import requests

# 온도,습도,기압,미세먼지,초미세먼지,CO2 6가지 환경정보 획득 및 저장

all_url = "http://192.168.123.101:5000/read-sensor"
JSONContent = requests.get(all_url).json()
bme_content = json.dumps(JSONContent, indent = 4, sort_keys=True)
print(bme_content)

dust_url = "http://192.168.123.101:5000/read-dust"
JSONContent = requests.get(dust_url).json()
dust_content = json.dumps(JSONContent, indent = 4, sort_keys=True)
print(dust_content)

co2_url = "http://192.168.123.100/getCo2"
JSONContent = requests.get(co2_url).json()
co2_content = json.dumps(JSONContent, indent = 4, sort_keys=True)
print(JSONContent[0]['sensor_val'])

def getDataFrame(frame_id, series_id):
    
    bme_url = "http://192.168.123.101:5000/read-sensor?task=getTemperature"
    dust_url = "http://192.168.123.101:5000/read-dust"
    co2_url = "http://192.168.123.100/getCo2"

    BMEContent = requests.get(bme_url).json()
    CO2Content = requests.get(co2_url).json()
    DustContent = requests.get(dust_url).json()
   
    data = [series_id, BMEContent[0]['timestamp'], BMEContent[0]['temperature'], BMEContent[0]['humidity'], 
                          BMEContent[0]['pressure'], CO2Content[0]['sensor_val'], DustContent[0]['PM25'], DustContent[0]['PM10']]
    print(data)
    frame_id.loc[series_id] = data
    #s1 = pd.Series(data, index=frame_id.columns)
    #frame_id.loc(s1)
    
    return frame_id

import time
i = 2600;
df = pd.DataFrame(columns=["id", "date", "temperature", "humidity", "pressure", "CO2", "PM2.5", "PM10" ])

while True:
    df = getDataFrame(df, i)
    i=i+1
    if(i%100 == 0):
        df.to_csv("dataset.csv",encoding='utf-8', doublequote=False, index=False, mode="a", header=False)
        df = df[0:0]
    time.sleep(1)
