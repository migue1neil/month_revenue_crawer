# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 18:26:10 2022

@author: user
"""

import requests
from bs4 import BeautifulSoup
import time as time
import random
import pandas as pd

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.3.1014788092.1639653982; _gid=GA1.3.53874647.1663498028; JSESSIONID=B8EBDCB41BFE2A7142BA081B897F5791',
    'Host': 'www.twse.com.tw',
    'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42'
}

month = ['01','02','03','04','05','06','07','08','09','10','11','12']
URL_list = []
for i in range(1999,2023):
    for j in month:
        URL = 'https://www.twse.com.tw/indicesReport/MI_5MINS_HIST?response=html&date='+str(i)+j+'01'
        URL_list.append(URL)

all_list = []
for url in URL_list:
    resp = requests.get(url,headers=headers)
    time.sleep(random.uniform(1.1,5.5))
    soup = BeautifulSoup(resp.text, 'html5lib')
    try:
        prices = soup.find('tbody').find_all('tr') #???
    except Exception as e:
        print('Exception: {}'.format(e))
    for price in prices:
        Daily_price = [s for s in price.stripped_strings]
        all_list.append(Daily_price)

tw_20 = pd.DataFrame(all_list, columns = ['Date', 'Open', 'Upper', 'Lower','Close'])

#這邊是把，改成空白
tw_20['Open'] = tw_20['Open'].str.replace(',','').astype(float)
tw_20['Upper'] = tw_20['Upper'].str.replace(',','').astype(float)
tw_20['Lower'] = tw_20['Lower'].str.replace(',','').astype(float)
tw_20['Close'] = tw_20['Close'].str.replace(',','').astype(float)















    