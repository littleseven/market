# -*- coding:utf-8 -*-

import requests
import pandas as pd
import bs4 as bs
import yfinance as yf
import time
import openpyxl

def get_spx():
    # url = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    # request = requests.get(url, headers=headers)
    with open('/Users/guoshuai/PycharmProjects/market-breadth/List_of_SP_500_companies.txt') as f:
        text = f.read()
        f.close()
    soup = bs.BeautifulSoup(text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})

    symbol_list = []
    name_list = []
    sector_list = []
    industry_list = []
    for i in table.findAll('tr')[1:]:
        symbol_list.append(i.find_all('td')[0].get_text().replace('\n', ''))
        name_list.append(i.find_all('td')[1].get_text().replace('\n', ''))
        sector_list.append(i.find_all('td')[3].get_text().replace('\n', ''))
        industry_list.append(i.find_all('td')[4].get_text().replace('\n', ''))
    return pd.DataFrame({'code': symbol_list, 'name': name_list, 'is_spx': 'Y', 'sp_sector': sector_list})


df = get_spx();
print(df);
df.columns = ['code','name','is_ppx','sp_sector']
#df.index = ['a','b','c','d','e','f','g','h','i','j']

writer = pd.ExcelWriter('../data/sp500.xlsx')
df.to_excel(writer)
writer.save()
