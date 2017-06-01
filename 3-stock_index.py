import json
from urllib.request import Request, urlopen
import re
import ssl
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import tzlocal

local_timezone = tzlocal.get_localzone()
req = Request('http://www.investing.com/indices/major-indices',
              headers={'User-Agent': 'Mozilla/5.0'})
# gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  # Only for gangstars
context = ssl._create_unverified_context()
page = urlopen(req, context=context).read()
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
        # print('length is five')
        # print(time)
        timereformatted = str(datetime.now())[0:8] + time[0:2] + " " + "17:00:00"
    elif len(time) == 8:
        # print('length is eight')
        # print(time)
        timereformatted = str(datetime.now())[0:10] + " " + time
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
        if index == "Nasdaq":
            try:
                utc_time = datetime.strptime(timereformatted, "%Y-%m-%d %H:%M:%S")
                local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
                local_time = str(local_time)[0:19]
                # print(local_time)
                t["Time"] = local_time
                result.append(t)
            except:
                pass

        elif index == "Hang Seng":
            try:
                utc_time = datetime.strptime(timereformatted, "%Y-%m-%d %H:%M:%S")
                local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
                local_time = str(local_time)[0:19]
                t["Time"] = local_time
                # print(local_time)
                result.append(t)
            except:
                pass
        elif index == "China A50":
            try:
                utc_time = datetime.strptime(timereformatted, "%Y-%m-%d %H:%M:%S")
                local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
                local_time = str(local_time)[0:19]
                t["Time"] = local_time
                # print(local_time)
                result.append(t)
            except:
                pass
        elif index == "Nikkei 225":
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
if status_code == 0:
    print(json.dumps({"DataList": {'Root': result}}, sort_keys=False))
else:
    print()
