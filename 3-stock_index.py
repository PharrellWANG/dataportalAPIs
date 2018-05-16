import json
import requests
import re
import ssl
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import tzlocal

local_timezone = tzlocal.get_localzone()
req = requests.get(
    'http://www.investing.com/indices/major-indices',
    headers={'User-Agent': 'Mozilla/5.0'}
)
page = req.content
soup = BeautifulSoup(page, 'lxml')
collection = soup.find_all("tr", id=lambda x: x and x.startswith('pair'))
# print(collection)
result = []
status_code = 0
time_format = re.compile('.{2}/.{2}')
time_format1 = re.compile('.{2}:.{2}:.{2}')
for i in collection:
    td_set = i.find_all('td')
    single_list = []
    for single in td_set:
        if single.text != u'\xa0':
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
        if len(time) == 5 or len(time) == 8:
            # print('----------------------------------------------------')
            # print(time)
            # print(len(time))
            # print(time_format.match(time))
            # print(time_format1.match(time))
            if time_format.match(time) or time_format1.match(time):
                pass
            else:
                status_code = 4
                break
        #
        # Below Handling can be omitted
        #
        # elif len(time) == 7:
        #     continue
        # else:
        #     status_code = 5
        #     break
    except IndexError:
        status_code = 6
    if len(time) == 5:
        # print('length is five ----------------------5')
        # print(time)
        timereformatted = str(datetime.now())[0:8] + time[0:2] + " " + "17:00:00"
        # print(timereformatted)
    elif len(time) == 8:
        # print('length is eight -------------------------------8')
        # print(time)
        timereformatted = str(datetime.now())[0:10] + " " + time
        # print(timereformatted)
    else:
        pass
    status = single_list[7]
    t["index"] = index
    t["Last"] = last
    t["High"] = high
    t["ChangeValue"] = changevalue
    t["RatioChanged"] = changeratio
    t["Status"] = status
    # t["Time"] = timereformatted
    # print(timereformatted)
    if status_code == 0:
        if index in ["Nasdaq", "Hang Seng", "China A50", "Nikkei 225"]:
            try:
                utc_time = datetime.strptime(timereformatted, "%Y-%m-%d %H:%M:%S")
                local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
                local_time = str(local_time)[0:19]
                # print(local_time)
                t["Time"] = local_time
                result.append(t)
            except:
                pass
        else:
            pass
    else:
        pass
# print(status_code)
if status_code == 0:
    print(json.dumps({"DataList": {'Root': result}}, sort_keys=False))
else:
    print(status_code)
