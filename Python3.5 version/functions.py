#coding=utf-8
import datetime
from datetime import datetime
from datetime import timedelta
import json
from urllib.parse import quote



def today():
    time = str(datetime.now())
    # print time
    date = time.split(" ")[0]
    day = date[5:]
    # print day
    return day


def yesterday():
    yest = datetime.now() - timedelta(days=1)
    date = str(yest).split(" ")[0]
    day = date[5:]
    # print day
    return day

def days_ago(n):
    yest = datetime.now() - timedelta(days=n)
    date = str(yest).split(" ")[0]
    day = date[5:]
    print(day)
    return day


def url_encoding(list):
    url_word_list = []
    for country in list:
        url_word_list.append(quote(country))
    return url_word_list



def create_url_list(list):
    url_list = []
    for country in list:
        this_url = "http://m.weibo.cn/container/getIndex?type=wb&queryVal=" + country + \
          "&luicode=10000011&lfid=106003type%3D1&title=" + country + \
          "&containerid=100103type%3D2%26q%3D" + country + "&page="
        url_list.append(this_url)
    return url_list



def format_datetime(time):
    this_date = time.split(' ')[0]
    this_time = time.split(' ')[1]
    mon = this_date.split('-')[0]
    day = this_date.split('-')[1]
    hor = this_time.split(':')[0]
    min = this_time.split(':')[1]
    return datetime(2017, int(mon), int(day), int(hor), int(min))


def get_this_endtime_text(content):
    this_data = content
    decoded_data = this_data.decode('utf-8')
    json_data = json.loads(decoded_data)
    try:
        this_endtime_text = json_data['data']['cards'][0]['card_group'][-1]['mblog']['created_at']
    except Exception as e:
        raise
    return this_endtime_text


def sleep_how_long(lag_hour, starttime, endtime):
    during = (endtime - starttime).total_seconds()
    lag_seconds = lag_hour * 3600
    during = lag_seconds - int(during)
    return during


