import json
from urllib.request import Request, urlopen
import re
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import tzlocal
local_timezone = tzlocal.get_localzone()
req = Request('http://www.investing.com/indices/major-indices',
              headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req).read()
soup = BeautifulSoup(page, 'lxml')
collection = soup.find_all("tr", id=lambda x: x and x.startswith('pair'))
result = []
status_code = 0
time_format = re.compile('.{2}/.{2}')
time_format1 = re.compile('.{2}:.{2}:.{2}')
for i in collection:
    td_set = i.find_all('td')
    single_list = []
    for single in td_set:
        if single.text != "\xa0":
            single_list.append(single.text)
    length = len(single_list)
    if length != 7:
        status_code = 1
        break
    icon = td_set[8].span
    icon_class = icon['class'][0]
    single_list.append(icon_class)
    t = {}
    index = single_list[0]
    last = single_list[1]
    high = single_list[2]
    changevalue = single_list[4]
    changeratio = single_list[5]
    try:
        time = single_list[6]
        if len(time) == 5 or 8:
            if time_format.match(time) or time_format1.match(time):
                pass
            else:
                status_code = 4
                break
        else:
            status_code = 5
            break
    except IndexError:
        status_code = 6
    if len(time) == 5:
        timereformatted = str(datetime.now())[0:8] + time[0:2] + " " + "17:00:00"
    elif len(time) == 8:
        timereformatted = str(datetime.now())[0:10] + " " + time
    else:
        pass
    status = single_list[7]
    t["Index"] = index
    t["Last"] = last
    t["High"] = high
    t["ValueChanged"] = changevalue
    t["RatioChanged"] = changeratio
    t["Status"] = status
    # t["Time"] = timereformatted
    if status_code == 0:
        if index == "Nasdaq":
            utc_time = datetime.strptime(timereformatted, "%Y-%m-%d %H:%M:%S")
            local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
            local_time = str(local_time)[0:19]
            print(local_time)
            t["Time"] = local_time
            result.append(t)
        elif index == "Hang Seng":
            utc_time = datetime.strptime(timereformatted, "%Y-%m-%d %H:%M:%S")
            local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
            local_time = str(local_time)[0:19]
            t["Time"] = local_time
            print(local_time)
            result.append(t)
        elif index == "China A50":
            utc_time = datetime.strptime(timereformatted, "%Y-%m-%d %H:%M:%S")
            local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
            local_time = str(local_time)[0:19]
            t["Time"] = local_time
            print(local_time)
            result.append(t)
        elif index == "Nikkei 225":
            utc_time = datetime.strptime(timereformatted, "%Y-%m-%d %H:%M:%S")
            local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
            local_time = str(local_time)[0:19]
            print(local_time)
            t["Time"] = local_time
            result.append(t)
        else:
            pass
    else:
        pass
if status_code == 0:
    print(json.dumps({"DataList": {'Root': result}}, sort_keys=False))
else:
    print()
