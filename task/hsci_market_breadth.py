# US 股市场宽度
import datetime
import os
import sys

from tools.util import *
from tools.mydb import *

path = os.path.dirname(__file__) + os.sep + '..' + os.sep
sys.path.append(path)


def market_breadth():
    df = mydb.read_from_sql('SELECT * FROM hsci_stocks_sector_d ORDER BY date desc;')
    mb_name = path + './data/Market-Breadth-HSCI-' + str(datetime.today().date()) + '.jpg'
    analysis.market_breadth(df, mb_name, 'hsc', '沪深港通市场宽度')
    mb_name = path + './data/Market-Breadth-HSCI-' + str(datetime.today().date()) + '-W.jpg'
    analysis.market_breadth_wide(df, mb_name, 'hsc', '沪深港通市场宽度')
    # analysis.recommend(df, 'TEC', mb_name)


if __name__ == '__main__':
    market_breadth()
