# -*- coding:utf-8 -*-

from opendatatools import usstock
import os
import sys
import yfinance as yf

# import xldr
import pandas as pds
from tools.util import *
from tools.mydb import *

path = os.path.dirname(__file__) + os.sep + '..' + os.sep
sys.path.append(path)


def fix_code(x):
    if isinstance(x, str):
        count = 4 - len(x)
        while count > 0:
            x = '0' + x
        return x + '.HK'
    elif isinstance(x, int):
        if x > 1000:
            y = str(x)
        elif x < 10:
            y = '000' + str(x)
        elif x < 100:
            y = '00' + str(x)
        elif x < 1000:
            y = '0' + str(x)
        return y + '.HK'
    else:
        return None


def get_sector(sector):
    sectors = {
        'Utilities': 'Utilities',
        'Consumer Cyclical': 'Consumer Discretionary',
        'Healthcare': 'Health Care',
        'Technology': 'Information Technology',
        'Consumer Defensive': 'Consumer Staples',
        'Financial Services': 'Financials',
        'Basic Materials': 'Materials',
        'Industrials': 'Industrials',
        'Real Estate': 'Real Estate',
        'Energy': 'Energy',
        'Communication Services': 'Communication Services'
    }
    return sectors.get(sector, None)


def get_industry(code):
    print(code)
    ticker = yf.Ticker(code)
    info = ticker.info
    return info['industry']


start = datetime.now()

info_table = 'hk_stocks_info'

# 更新 标普500 权重股
hk_columns = ['code', 'name']
columns = ['code', 'name', 'sector', 'industry', 'is_hs', 'sp_sector']

sql = ''' SELECT `{}` FROM `{}` WHERE sector != '' AND sector is not null;''' \
    .format('`,`'.join(columns), info_table)
data = mydb.read_from_sql(sql)

symbols = pds.read_excel(path + './data/hk380.xls', sheet_name='Sheet3', encoding='utf8')

if symbols is not None:
    symbols.rename(columns={'code': 'code', 'name': 'name', 'sector': 'sector', 'industry': 'industry'},
                   inplace=True)
    symbols = symbols[hk_columns].set_index(['code']).drop_duplicates().reset_index()
    symbols.code = symbols.code.map(fix_code)

    if data is not None:
        symbols = pd.merge(symbols, data, on=['code', 'name'], how='left')
    symbols['is_hs'] = 'Y'
    mydb.upsert_table(info_table, columns, symbols)
    codes = symbols[symbols['sector'].isnull()].code
    for code in codes:
        print(code)
        ticker = yf.Ticker(code)
        info = ticker.info
        if info is not None:
            symbols.loc[symbols.code == code, 'sector'] = info['sector']
            symbols.loc[symbols.code == code, 'sp_sector'] = get_sector(info['sector'])
            symbols.loc[symbols.code == code, 'industry'] = info['industry']
            mydb.upsert_table(info_table, columns, symbols.loc[symbols.code == code])

    symbols.sp_sector = symbols.sector.map(get_sector)
    # mydb.truncate_table(info_table)
    mydb.upsert_table(info_table, columns, symbols)


end = datetime.now()
print('Download Data use {}'.format(end - start))
