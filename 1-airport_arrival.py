from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import json

req = Request('http://www.hongkongairport.com/flightinfo/eng/real_arrinfo.do',
              headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req).read()

soup = BeautifulSoup(page, 'lxml')
for x in soup.find_all("td"):
    if len(x.text) == 0:
        x.extract()
for y in soup.find_all(mr='true'):
    y.extract()
collection = soup.find_all("tr")
time_format = re.compile('.{2}:.{2}')
result = []
status_code = 0  # only status == 0 is good to go
for i in collection:
    t = {}
    s = {}
    td_set = i.find_all('td')
    length = len(i.find_all('td'))
    if length != 6:  # tag numbers should be 6
        status_code = 1
        s["status"] = status_code
        break
    single_list = []
    for single in td_set:
        single_list.append(single.text)
    try:
        data = single_list[3]
    except IndexError:
        status_code = 2
        s["status"] = status_code
        break
    try:
        data1 = single_list[1]
    except IndexError:
        print("Exception detected from data source, please contact API administrator. Error NO: 3.0")
        status_code = 3
        s["status"] = status_code
        break
    fields = data.split(",")
    fields1 = data1.split(",")
    selection = fields[1]
    selection1 = fields1[0]
    try:
        time = single_list[0]
        if len(time) == 5:
            if time_format.match(time):
                pass
            else:
                status_code = 4
                s["status"] = status_code
                break
        else:
            status_code = 5
            s["status"] = status_code
            break
    except IndexError:
        status_code = 6
        s["status"] = status_code
        break
    flight = selection1
    try:
        origin = single_list[2]
    except IndexError:
        status_code = 7
        s["status"] = status_code
        break
    airline = selection
    try:
        status = single_list[5][0:13]
    # changes made in the above line
    except IndexError:
        status_code = 8
        s["status"] = status_code
        break
    if status != '\xa0':
        t["Time"] = time
        t["Flight"] = flight
        t["Origin"] = origin
        t["Airline"] = airline
        t["Status"] = status
        result.append(t)
if status_code == 0:
    print(json.dumps({"DataList": {'Root': result}}, sort_keys=False))
else:
    print()
# print(json.dumps({'status': status_code, 'data': result}, sort_keys=False))
