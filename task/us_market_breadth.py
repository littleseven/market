# US 股市场宽度
import datetime
import os
import sys

path = os.path.dirname(__file__) + os.sep + '..' + os.sep
sys.path.append(path)

from tools.util import *
from tools.mydb import *

list_sql = '''
            select * from us_stocks_info
            where total_cap > 10 or is_spx = 'Y' or is_ndx = 'Y' or is_dji = 'Y';
           '''

df = mydb.read_from_sql('SELECT * FROM us_stocks_sector_d ORDER BY date desc;')
mb_name = path + './data/Market-Breadth-US-' + str(datetime.today().date()) + '.jpg'
analysis.market_breadth(df, mb_name)