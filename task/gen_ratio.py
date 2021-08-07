# coding=utf-8
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import ticker

from tools.util import *
from tools.mydb import *

from tools.util import date, yf


class Stock:
    def __init__(self, code, name):
        self.code = code
        self.name = name

plt.rcParams['font.family'] = 'SongTi SC'
plt.rcParams['axes.unicode_minus'] = False

stocks = [
    # 香港行业

    Stock('HSI', u'恒生指数'),
    Stock('QQQ', u'纳斯达克指数'),
    Stock('CQQQ', u'中国科技指数'),
    Stock('KWEB', u'中国互联网指数'),
    Stock('ARKK', u'ARKK'),
    # Stock('BK1077.HK', u'铜'),
    # Stock('FEM2106.HK', u'铁矿石'),
    # Stock('GDU2106.HK', u'黄金'),

    # Stock('0700.HK', u'腾讯'),
    # Stock('1211.HK', u'比亚迪'),
    # Stock('0981.HK', u'中芯国际'),
    # Stock('1810.HK', u'小米集团'),
    # Stock('3606.HK', u'福耀玻璃'),
    # Stock('6862.HK', u'海底捞'),
    # Stock('HK.02333', u'长城汽车'),
    # Stock('2382.HK', u'舜禹光学'),
    # Stock('3690.HK', u'美团'),
    # Stock('9888.HK', u'百度'),
    # Stock('800000.HK', u'恒生指数'),
    # Stock('800700.HK', u'恒生科技')
]

start = '2021-1-13'
# end = '2021-05-22'
end = str(datetime.today().date())
max_count = 300

figure = pd.DataFrame()
# std, figure['key'] = get_base_value('HK.800000', start, end, max_count)

ratio = []
sub_codes = stocks[0: len(stocks)]
symbol_list = []
for stock in stocks:
    symbol_list.append(stock.code)


data = yf.download(symbol_list, start=date.get_9month_ago(), end=date.get_end_day(),
                   group_by="ticker", threads=True, auto_adjust=True,
                   interval='1d')

for i in stocks:
    if i.code in data.columns:
        df = data[i.code]
        if df is None:
            continue
        df = df.tail(250)
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
        figure[i.name] = (df['close'] - df['close'][df.index[0]])/df['close'][df.index[0]]
        ratio.append(i.name)
        print(i.name)
figure.plot(x='date', y=ratio)
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=1))

plt.show()