# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 14:57:06 2022

@author: Neil
"""

#finlab 的月營收爬蟲教學，只有上市公司

import pandas as pd
import requests
from io import StringIO
import time
import random
from datetime import datetime
def monthly_report( year , month , exchange_code , country_code ):
    
    # 假如是西元，轉成民國
    if year > 1990:
        year -= 1911
    
    url = "https://mops.twse.com.tw/nas/t21/"+ str(exchange_code) +"/t21sc03_"+str(year)+'_'+str(month)+"_"+ str(country_code)+".html"
    if year <= 98:
        url = "https://mops.twse.com.tw/nas/t21/"+ str(exchange_code) +"/t21sc03_"+str(year)+'_'+str(month)+'.html'
    
    # 偽瀏覽器
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    # 下載該年月的網站，並用pandas轉換成 dataframe
    # header = 是指偽裝成瀏覽器格式跟伺服器互動
    r = requests.get(url, headers=headers) 
    r.encoding = 'big5'

    dfs = pd.read_html(StringIO(r.text), encoding='big-5')

    df = pd.concat([df for df in dfs if df.shape[1] <= 11 and df.shape[1] > 5])
    
    if 'levels' in dir(df.columns):
        df.columns = df.columns.get_level_values(1)
    else:
        df = df[list(range(0,10))]
        column_index = df.index[(df[0] == '公司代號')][0]
        df.columns = df.iloc[column_index]
    
    df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')
    df = df[~df['當月營收'].isnull()] #選出不是空值的股票
    df = df[df['公司代號'] != '合計']
    df = df[df['公司代號'] != '全部國內上市公司合計']
    df = df[df['公司代號'] != '全部國外上市公司合計']
    df = df[df['公司代號'] != '全部國內上櫃公司合計']
    df = df[df['公司代號'] != '全部國外上櫃公司合計']

    df["年月"] = str(year) + "/" + ("%02d" % month) # 加入該月的時間標籤
    if exchange_code == "sii" :
        df["上市別"] = "TSE"
    elif exchange_code == "otc" :
        df["上市別"] = "OTC"
    elif exchange_code == "rotc" :
        df["上市別"] = "ROTC"
    else:
        df["上市別"] = ""      
    # 偽停頓
    time.sleep(random.uniform(1.1,5.4))

    return df


#####
aa = monthly_report(2022, 8 , "sii" , 1)

year = range(2010,2023) # range最後面的數字沒有包含
month = range(1,13)
market  = ("sii" , "otc") #pub是公開發行公司 ，rotc是興櫃公司
country  = ("0" , "1" ) # 0 是國內公司 ， 1 是國外公司(KY,DR)    

start = datetime.now()
month_revenue = pd.DataFrame()
for i in year : 
    for j in month: 
        for k in market : # 切換市場
            for l in country : # 切換國內國外
                try:
                    month_revenue = month_revenue.append(monthly_report( i , j , k , l))
                except Exception as e:
                    print( i , j , k , l ,sep = ",")
                    print('Exception: {}'.format(e))
                    
print(datetime.now() - start)      
        
month_revenue.to_csv("month_revenue.csv" , sep = "," ,index = False , encoding = "utf-8")
        
##### 月營收爬蟲 資料更新
# =============================================================================
# market  = ("sii" , "otc") #pub是公開發行公司 ，rotc是興櫃公司
# country  = ("0" , "1" ) # 0 是國內公司 ， 1 是國外公司(KY,DR)    
# 
# old_month_revenue = pd.read_csv("month_revenue.csv" , encoding = "utf-8")
# old_month_revenue[["年","月"]] = old_month_revenue.年月.str.split("/" , expand = True).astype(int)
# latest = old_month_revenue["年"].max()
# #old_month_revenue.info()
# gap = datetime.now().year - 1911 - latest 
# year = range(latest,gap+1) # range最後面的數字沒有包含
# month = range(1,13)
# market  = ("sii" , "otc") #pub是公開發行公司 ，rotc是興櫃公司
# country  = ("0" , "1" ) # 0 是國內公司 ， 1 是國外公司(KY,DR)  
# 
# 
# new_month_revenue = pd.DataFrame()
# for i in year:  # 年
#     for j in month:         # 月
#         for k in market: # 市場
#             for l in country: # 國內國外
#                 try:
#                     new_month_revenue = new_month_revenue.append(monthly_report( i , j , k , l))
#                 except Exception as e:
#                     print( i , j , k , l ,sep = ",")
#                     print('Exception: {}'.format(e))
# 
# updated_month_revenue = old_month_revenue.append(new_month_revenue , index = False )
# updated_month_revenue = updated_month_revenue.drop_duplicates()
# updated_month_revenue.to_csv("updated_month_revenue" , encoding = "utf-8")
#  
# =============================================================================
