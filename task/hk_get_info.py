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

def us_total_cap(x):
    if isinstance(x, str) and x.endswith('B'):
        return float(x[1:-1]) * 10
    elif isinstance(x, str) and x.endswith('M'):
        return float(x[1:-1]) / 100
    else:
        return None

start = datetime.now()

info_table = 'hk_stocks_info'
mydb.truncate_table(info_table)

# 更新 标普500 权重股
hk_columns = ['code', 'name', 'sector', 'weight']
symbols = pds.read_excel(path + './data/hk380.xls', sheet_name='Sheet2', encoding='utf8')

if symbols is not None:
    columns = ['code', 'name', 'sector', 'is_hs', 'hs_weight']
    symbols.rename(columns={'code': 'code', 'name': 'name', 'sector': 'sector', 'weight': 'hs_weight'},
                   inplace=True)
    symbols['is_hs'] = 'Y'
    symbols = symbols[columns].set_index(['code']).drop_duplicates().reset_index()
    # symbols.total_cap = symbols.total_cap.map(us_total_cap)
    mydb.upsert_table(info_table, columns, symbols)

end = datetime.now()
print('Download Data use {}'.format(end - start))
