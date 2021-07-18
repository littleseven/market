# -*- coding:utf-8 -*-
import math

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
    if math.isnan(x):
        return None
    elif isinstance(x, int) or isinstance(x, float):
        x = int(x)
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


def fix_acode(x):
    if math.isnan(x):
        return None
    elif isinstance(x, int) or isinstance(x, float):
        x = int(x)
        if 600000 <= x < 700000:
            y = str(x) + '.SS'
        elif 10000 <= x < 600000:
            y = str(x) + '.SZ'
        elif 1000 <= x < 10000:
            y = '00' + str(x) + '.SZ'
        elif 100 <= x < 1000:
            y = '000' + str(x) + '.SZ'
        elif 10 <= x < 100:
            y = '0000' + str(x) + '.SZ'
        elif 0 < x < 10:
            y = '00000' + str(x) + '.SZ'
        return y
    else:
        return None


def get_code(c, a, h):
    if c is not None:
        return c
    elif h is not None:
        return h
    elif a is not None:
        return a


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


def is_ss(x):
    if isinstance(x, str) and x.endswith('SS'):
        return 'Y'
    else:
        return 'N'


def is_sz(x):
    if isinstance(x, str) and x.endswith('SZ'):
        return 'Y'
    else:
        return 'N'


def is_hs(x):
    if isinstance(x, str) and x.endswith('HK'):
        return 'Y'
    else:
        return 'N'


start = datetime.now()

info_table = 'hsc_stocks_info'
columns = ['code', 'name', 'sector', 'industry', 'is_hs', 'sp_sector']

sql = ''' SELECT `{}` FROM `{}` WHERE sector != '' AND sector is not null;''' \
    .format('`,`'.join(columns), info_table)
data = mydb.read_from_sql(sql)

# 更新 标普500 权重股
hk_columns = ['code', 'name']
symbols = pds.read_excel(path + './data/hsc500c.xls', sheet_name='Sheet4', encoding='utf8')
# 'acode', 'hcode'
if symbols is not None:
    symbols.rename(columns={'code': 'code', 'name': 'name', 'sector': 'sector', 'industry': 'industry'},
                   inplace=True)
    # symbols['is_hs'] = 'Y'
    # symbols['sector'] = ''
    # symbols['industry'] = ''
    # symbols['sp_sector'] = ''
    symbols.hcode = symbols.hcode.map(fix_code)
    symbols.code = symbols.code.map(fix_code)
    symbols.acode = symbols.acode.map(fix_acode)
    symbols.code = symbols.apply(lambda row: get_code(row['code'], row['acode'], row['hcode']), axis=1)
    symbols['is_hs'] = symbols.code.map(is_hs)
    symbols['is_ss'] = symbols.code.map(is_ss)
    symbols['is_sz'] = symbols.code.map(is_sz)
    # codes = symbols.code #[0:10]
    # mydb.upsert_table(info_table, columns, symbols)
    if data is not None:
        symbols = pd.merge(symbols, data, on=['code', 'name'], how='left')

    mydb.upsert_table(info_table, columns, symbols)
    codes = symbols[symbols['sector'].isnull()].code
    # codes = symbols[symbols['sector'] == ''].code
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
