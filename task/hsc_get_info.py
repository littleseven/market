# -*- coding:utf-8 -*-

from opendatatools import usstock
import os
import sys
# import xldr
import pandas as pds

path = os.path.dirname(__file__) + os.sep + '..' + os.sep
sys.path.append(path)

from tools.util import *
from tools.mydb import *


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
mydb.truncate_table(info_table)

# 更新 标普500 权重股
symbols = pds.read_excel(path + './data/hsc500c.xls', sheet_name='Sheet1', encoding='utf8')

if symbols is not None:
    columns = ['code', 'name', 'sector', 'is_hs', 'is_ss', 'is_sz', 'weight']
    symbols.rename(columns={'code': 'code', 'name': 'name', 'sector': 'sector'},
                   inplace=True)
    symbols['is_hs'] = symbols.code.map(is_hs)
    symbols['is_ss'] = symbols.code.map(is_ss)
    symbols['is_sz'] = symbols.code.map(is_sz)
    #
    # symbols['hs_weight'] = symbols['weight']
    # symbols['ss_weight'] = symbols['weight']
    # symbols['sz_weight'] = symbols['weight']

    symbols = symbols[columns].set_index(['code']).drop_duplicates().reset_index()
    # symbols.total_cap = symbols.total_cap.map(us_total_cap)
    mydb.upsert_table(info_table, columns, symbols)

end = datetime.now()
print('Download Data use {}'.format(end - start))
