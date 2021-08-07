# coding=utf-8
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import ticker

from tools.util import *
from tools.mydb import *

from tools.util import date, yf


def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


class Stock:
    def __init__(self, code, name):
        self.code = code
        self.name = name

plt.rcParams['font.family'] = 'SongTi SC'
plt.rcParams['axes.unicode_minus'] = False

stocks = [
    # 香港行业
    #
    # Stock('HSI', u'恒生指数'),
    Stock('^GSPC', u'标普500'),
    # Stock('QQQ', u'纳斯达克指数'),
    # Stock('CQQQ', u'中国科技指数'),
    # Stock('KWEB', u'中国互联网指数'),
    Stock('GC=F', u'黄金'),
    Stock('CL=F', u'原油'),
    Stock('HG=F', u'铜'),
    # Stock('ARKK', u'ARKK'),
]

start = '2021-1-13'
# end = '2021-05-22'
end = str(datetime.today().date())
max_count = 300

figure = pd.DataFrame()
close = pd.DataFrame()
ratio = []
sub_codes = stocks[0: len(stocks)]
symbol_list = []
for stock in stocks:
    symbol_list.append(stock.code)


data = yf.download(symbol_list, start=date.get_2year_ago(), end=date.get_end_day(),
                   group_by="ticker", threads=True, auto_adjust=True,
                   interval='1d')

for i in stocks:
    if i.code in data.columns:
        df = data[i.code]
        if df is None:
            continue
        df = df.reset_index()
        df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low',
                           'Close': 'close', 'Volume': 'vol'},
                  inplace=True)
        df = df[~np.isnan(df['close'])]
        df['code'] = i.code
        df['name'] = i.name
        # df = analysis.stock_analysis(df, 20, 60, 120)
        if df is None:
            continue
        figure['date'] = df['date']

        if i.code == 'HG=F':
            close['copper'] = df['close']
        elif i.code == 'CL=F':
            close['oil'] = df['close']
        elif i.code == 'GC=F':
            close['gold'] = df['close']

        figure[i.name] = (df['close'] - df['close'][df.index[0]])/df['close'][df.index[0]]
        ratio.append(i.name)
        print(i.name)

figure['铜金比'] = normalization(close['copper']/close['gold'])
figure['油金比'] = normalization(close['oil']/close['gold'])
ratio.append('铜金比')
ratio.append('油金比')

figure.plot(x='date', y=ratio)
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=1))
plt.show()