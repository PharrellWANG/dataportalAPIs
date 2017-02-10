# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import json

req1 = Request('http://m.accuweather.com/en/hk/hong-kong/1123655/hourly-weather-forecast/1123655?day=1')
page1 = urlopen(req1).read()
req2 = Request('http://m.accuweather.com/en/hk/hong-kong/1123655/hourly-weather-forecast/1123655?day=2')
page2 = urlopen(req2).read()
soup1 = BeautifulSoup(page1, 'lxml')
soup2 = BeautifulSoup(page2, 'lxml')
letters1 = soup1.find_all("div", class_="wx-cell")
letters2 = soup2.find_all("div", class_="wx-cell")
result = []
status_code = 0  # only status_code = 0 is good to go
hour_format = re.compile('.{2}AM' or '.AM')
for element1 in letters1:
    t = {}
    s = {}
    tag = element1
    hour = (element1.a.get_text())[0:4]
    temp = (tag.find(class_="temp").get_text())[0:2]
    LastTwoCharInHour = hour[-2:]
    if LastTwoCharInHour == 'AM' or 'M':
        t["Time"] = hour
        status_code = 0
    else:
        status_code = 1
        break
    try:
        # print(temp)
        temp_val = int(temp)
        t["Temperature"] = temp
        status_code = 0
    except ValueError:
        # print("here we are")
        status_code = 2  # temp is not an int number
        break
    result.append(t)

for element2 in letters2:
    t = {}
    s = {}
    tag = element2
    hour = (element2.a.get_text())[0:4]
    temp = (tag.find(class_="temp").get_text())[0:2]
    LastTwoCharInHour = hour[-2:]
    if LastTwoCharInHour == 'AM' or 'M':
        t["Time"] = hour
        status_code = 0
    else:
        status_code = 1
        break
    try:
        try:
            temp_val = int(temp)
        except ValueError:
            temp = temp[-2:-1]
            print("here we go")
            print(temp)
            print(hour)
            temp_val = int(temp)
            print(temp_val)
        temp_val = int(temp)
        t["Temperature"] = temp
        status_code = 0
    except ValueError:
        status_code = 2  # temp is not an int number
        break
    result.append(t)
result[0]['Time'] = 'Now'
X_result = result[0:9]
if status_code == 0:
    print(json.dumps({"DataList": {'Root': X_result}}, sort_keys=False))
else:
    print(status_code)
