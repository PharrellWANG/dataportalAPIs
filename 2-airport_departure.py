from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import json

req = Request('http://www.hongkongairport.com/flightinfo/eng/real_depinfo.do',
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
    if length != 8:  # tag numbers should be 6
        status_code = 1
        s["status"] = status_code
        break
    single_list = []
    for single in td_set:
        single_list.append(single.text)
    data = single_list[6]
    data1 = single_list[1]
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
                status_code = 2
                s["status"] = status_code
                break
        else:
            status_code = 3
            s["status"] = status_code
            break
    except IndexError:
        status_code = 4
        s["status"] = status_code
        break
    flight = selection1
    des = single_list[2]
    airline = selection
    if "Dep" in single_list[7]:
        status = single_list[7][0:9]
    elif "Gate" in single_list[7]:
        status = single_list[7][0:11]
    elif "BoardingSoon" in single_list[7]:
        status = single_list[7][0:12]
    elif "Final" in single_list[7]:
        status = single_list[7][0:10]
    if status != '\xa0':
        t["Time"] = time  #
        t["Flight"] = flight  #
        t["destination"] = des  #
        t["Airline"] = airline  #
        t["Status"] = status  #
        result.append(t)
if status_code == 0:
    print(json.dumps({"DataList": {'Root': result}}, sort_keys=False))
else:
    print()
    # print(json.dumps({'status': status_code, 'data': result}, sort_keys=False))
