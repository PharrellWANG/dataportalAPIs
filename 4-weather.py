from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from pprint import pprint
from collections import defaultdict
import sys
import re
import json

req = Request('http://m.accuweather.com/en/hk/hong-kong/1123655/hourly-weather-forecast/1123655?day=2')
page = urlopen(req).read()

soup = BeautifulSoup(page, 'lxml')

letters = soup.find_all("div", class_="wx-cell")

result = []
status_code = 0 # only status_code = 0 is good to go

hour_format = re.compile('.{2}AM'or'.AM')

for element in letters:
    t = {}
    s = {}
    tag = element
    hour = (element.a.get_text())[0:4]
    temp = (tag.find(class_="temp").get_text())[0:2]
    LastTwoCharInHour = hour[-2:]
    if LastTwoCharInHour == 'AM' or 'M':
        t["time"] = hour
        status_code = 0
    else:
        status_code = 1
        break
    try:
        temp_val = int(temp)
        t["temperature"] = temp
        status_code = 0
    except ValueError:
        status_code = 2 # temp is not an int number
        break
    result.append(t)
print(json.dumps({'status': status_code, 'data': result}, sort_keys=False))

