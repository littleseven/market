# US 股市场宽度
import datetime
import os
import sys

from tools.util import *
from tools.mydb import *

path = os.path.dirname(__file__) + os.sep + '..' + os.sep
sys.path.append(path)


def market_breadth():
    df = mydb.read_from_sql('SELECT * FROM cn_stocks_sector_d ORDER BY date desc;')
    mb_name = path + './data/Market-Breadth-CN-' + str(datetime.today().date()) + '.jpg'
    analysis.market_breadth(df, mb_name, 'cn')
    # analysis.recommend(df, 'TEC', mb_name)


if __name__ == '__main__':
    market_breadth()
