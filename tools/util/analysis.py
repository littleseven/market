# -*- coding:utf-8 -*-

import talib as ta
import numpy as np
import pandas as pd
import dataframe as df
from matplotlib import pyplot as plt
from matplotlib import colors
import seaborn as sns
import imgkit


def stock_ma(data, short, mid, long):
    data = data.set_index(['date']).sort_index()
    close = data.close.values
    data.loc[:, 's_ma'] = ta.SMA(close, timeperiod=short)
    data.loc[:, 'm_ma'] = ta.SMA(close, timeperiod=mid)
    data.loc[:, 'l_ma'] = ta.SMA(close, timeperiod=long)

    data.loc[:, 's_ema'] = ta.EMA(close, timeperiod=short)
    data.loc[:, 'm_ema'] = ta.EMA(close, timeperiod=mid)
    data.loc[:, 'l_ema'] = ta.EMA(close, timeperiod=long)

    data.loc[:, 'cs'] = (data['close'] - data['s_ma']) / data['s_ma'] * 100
    data.loc[:, 'sm'] = (data['s_ma'] - data['m_ma']) / data['m_ma'] * 100
    data.loc[:, 'ml'] = (data['m_ma'] - data['l_ma']) / data['l_ma'] * 100
    data.loc[:, 'bais'] = data['cs'] + data['sm'] + data['ml']

    data.loc[:, 'ecs'] = (data['close'] - data['s_ema']) / data['s_ema'] * 100
    data.loc[:, 'esm'] = (data['s_ema'] - data['m_ema']) / data['m_ema'] * 100
    data.loc[:, 'eml'] = (data['m_ema'] - data['l_ema']) / data['l_ema'] * 100
    data.loc[:, 'ebais'] = data['ecs'] + data['esm'] + data['eml']
    return data.reset_index()


def stock_vol(data, short):
    data = data.set_index(['date']).sort_index()
    data['vol'] = data['vol'].replace(np.nan, 0)
    vol = data.vol.values
    vol = vol.astype(float)
    data.loc[:, 'ma_vol'] = ta.SMA(vol, timeperiod=short)
    data.loc[:, 'vol_rate'] = data['vol'] / data['ma_vol']
    return data.reset_index()


def stock_amount(data, short):
    data = data.set_index(['date']).sort_index()
    data['amount'] = data['amount'].replace(np.nan, 0)
    amount = data.amount.values
    amount = amount.astype(float)
    data.loc[:, 'ma_amt'] = ta.SMA(amount, timeperiod=short)
    data.loc[:, 'amt_rate'] = data['amount'] / data['ma_amt']
    return data.reset_index()


def is_gap(h, l, c, p_h, p_l, p_c):
    if c is None or p_c is None:
        return 'N'
    elif c > p_c:
        return "Y" if l > p_h else "N"
    else:
        return "Y" if h < p_l else "N"


def is_over(x, px):
    if x is None or px is None:
        return 'N'
    elif x > 0 and px < 0:
        return 'Y'
    else:
        return 'N'


def stock_gap_and_over(data):
    data[["date"]] = data[["date"]].astype(str)
    data['row_num'] = data.date.rank(method='min').astype(int)
    data_copy = data.copy()
    data_copy.row_num = data_copy.row_num.apply(lambda x: x + 1)
    data_copy.rename(columns={'open': 'pre_open', 'high': 'pre_high', 'low': 'pre_low', 'close': 'pre_close',
                              'cs': 'pcs', 'sm': 'psm', 'ml': 'pml', 'ecs': 'pecs', 'esm': 'pesm', 'eml': 'peml'
                              },
                     inplace=True)
    data_copy = data_copy[['code', 'row_num', 'pre_open', 'pre_high', 'pre_low', 'pre_close',
                           'pcs', 'psm', 'pml', 'pecs', 'pesm', 'peml'
                           ]]
    data = data.set_index(['code', 'row_num'])
    data_copy = data_copy.set_index(['code', 'row_num'])
    data = pd.merge(data, data_copy, how='left', on=['code', 'row_num'])

    data['is_gap'] = data.apply(
        lambda row: is_gap(row['high'], row['low'], row['close'], row['pre_high'], row['pre_low'], row['pre_close']),
        axis=1, raw=True)
    data['is_esm_over'] = data.apply(
        lambda row: is_over(row['esm'], row['pesm']),
        axis=1, raw=True)
    data['is_eml_over'] = data.apply(
        lambda row: is_over(row['eml'], row['peml']),
        axis=1, raw=True)
    data['is_cs_over'] = data.apply(
        lambda row: is_over(row['cs'], row['pcs']),
        axis=1, raw=True)
    data['is_sm_over'] = data.apply(
        lambda row: is_over(row['sm'], row['psm']),
        axis=1, raw=True)
    data['is_ml_over'] = data.apply(
        lambda row: is_over(row['ml'], row['pml']),
        axis=1, raw=True)
    return data.reset_index()


def is_turn_up(c, p_c, c_ago, p_c_ago):
    if p_c_ago is None or c_ago is None:
        return 'N'
    elif c > c_ago and p_c < p_c_ago:
        return "Y"
    else:
        return "N"


def stock_turn_up(data, c, day):
    data[["date"]] = data[["date"]].astype(str)
    data['row_num'] = data.date.rank(method='min').astype(int)
    data_copy = data.copy()
    data_copy.row_num = data_copy.row_num.apply(lambda x: x + day)
    close_ago = '{}_close'.format(c)
    pre_close_ago = '{}_pre_close'.format(c)
    data_copy.rename(columns={'close': close_ago, 'pre_close': pre_close_ago},
                     inplace=True)
    data_copy = data_copy[['code', 'row_num', close_ago, pre_close_ago]]
    data = data.set_index(['code', 'row_num'])
    data_copy = data_copy.set_index(['code', 'row_num'])
    data = pd.merge(data, data_copy, how='left', on=['code', 'row_num'])

    column = 'is_{}_up'.format(c)
    data[column] = data.apply(
        lambda row: is_turn_up(row['close'], row['pre_close'], row[close_ago], row[pre_close_ago]),
        axis=1, raw=True)
    return data.reset_index()


def stock_analysis(data, short, mid, long):
    if data is None or data.empty or data.date.size < long + 1:
        return None

    stk_columns = ['date', 'code', 'open', 'high', 'low', 'close', 'vol']
    data = data[stk_columns]
    data = stock_vol(data, short)
    data = stock_ma(data, short, mid, long)
    data = stock_gap_and_over(data)
    data = stock_turn_up(data, 's', short)
    data = stock_turn_up(data, 'm', mid)
    data = stock_turn_up(data, 'l', long)
    return data


def stock_zh_analysis(data, short, mid, long):
    if data is None or data.empty or data.date.size < long + 1:
        return None

    stk_columns = ['date', 'ts_code', 'code', 'open', 'high', 'low', 'close', 'vol', 'amount']
    data = data[stk_columns]
    data = stock_vol(data, short)
    data = stock_amount(data, short)
    data = stock_ma(data, short, mid, long)
    data = stock_gap_and_over(data)
    data = stock_turn_up(data, 's', short)
    data = stock_turn_up(data, 'm', mid)
    data = stock_turn_up(data, 'l', long)
    return data


def _background_gradient(s, m, M, cmap='PuBu', low=0, high=0):
    rng = M - m
    norm = colors.Normalize(m - (rng * low),
                            M + (rng * high))
    normed = norm(s.values)
    c = [colors.rgb2hex(x) for x in plt.cm.get_cmap(cmap)(normed)]
    return ['background-color: %s' % color for color in c]


def _border_blank(data):
    return pd.Series('border-left: thick solid white', index=data.index)


def market_breadth(data, file, market='us', title=None):
    if data is None or data.empty:
        return None
    cm = sns.diverging_palette(10, 130, as_cmap=True)
    options = {'encoding': "UTF-8", 'width': 590}
    data = data.set_index('date')
    data = data.drop(data[data.isnull().T.any()].index)
    data = data.astype(int)
    text = dict(selector="th", props=[('text-align', 'center'),
                                      ('font-weight', 'bold'),
                                      ('font-size', '15px'),
                                      ('color', 'black'),
                                      ('border-right', 'thick solid white'),
                                      ])
    table = dict(selector="", props=[('border-spacing', '0px'),
                                     ('border-collapse', 'collapse')
                                     ])
    print([text, table])

    if title is not None:
        caption = title
    elif market == 'hk':
        caption = '港股市场宽度'
    elif market == 'hsc':
        caption = '沪深港通市场宽度'
    elif market == 'us':
        caption = '美股市场宽度'
    elif market == 'cn':
        caption = 'A股通300市场宽度'
    else:
        caption = '市场宽度'

    html = data.style \
        .apply(_background_gradient, cmap=cm, m=0, M=100)\
        .apply(_background_gradient, cmap=cm, m=0, M=1100, subset='SUM') \
        .apply(_border_blank, subset='SUM') \
        .set_properties(**{'text-align': 'center'}) \
        .set_caption(caption) \
        .set_table_styles([text, table]) \
        .render(width=800)
    # print(html.split('\n'))
    imgkit.from_string(html, file, options=options)
    print(html.split('\n')[0:10])


def market_breadth_wide(data, file, market='us', title=None):
    if data is None or data.empty:
        return None
    cm = sns.diverging_palette(10, 130, as_cmap=True)
    options = {'encoding': "UTF-8", 'width': 1000}
    data = data.set_index('date')
    data = data.drop(data[data.isnull().T.any()].index)
    data = data.astype(int)
    head = dict(selector="th", props=[('text-align', 'center'),
                                      ('color', 'black'),
                                      ('font-weight', 'bold'),
                                      ('font-size', '1px'),
                                      ('border', '0px solid green'),
                                      ('margin', '0px')
                                      ])
    text = dict(selector="td", props=[('text-align', 'center'),
                                      ('color', 'black'),
                                      ('font-size', '0px'),
                                      ('font-weight', 'normal'),
                                      ('border', '0px solid blue'),
                                      ('margin', '0px')
                                      ])
    index = dict(selector="caption", props=[('caption-side', 'bottom'),
                                            ('font-size', '1.25em')
                                            ])
    table = dict(selector="", props=[('border-spacing', '1px'),
                                     ('border-collapse', 'collapse')
                                            ])
    print([text, index])

    data = data.sort_values(by='date', ascending=True)
    # data = data.reset_index(drop=True)

    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)

    # .hide_index()
    data.reset_index()
    # date = data['date']
    # data = data.drop('date', axis=1)
    # data.insert(12, 'date', date)
    data = data.T
    html = data.style \
        .apply(_background_gradient, cmap=cm, m=0, M=100) \
        .apply(_background_gradient, cmap=cm, m=0, M=1100, subset=pd.IndexSlice['SUM', :]) \
        .set_properties(**{'width': '50px', 'height': '8px', 'font-size': '10px'}) \
        .set_table_styles([table, head, text, index]) \
        .render(width=1000)
    # print(html.split('\n')[0:100])
    f = open(file + '.html', 'w')
    f.write(html)
    f.close()
    imgkit.from_string(html, file, options=options)


def recommend(data, index_columns, file):
    if data is None or data.empty:
        return None

    options = {'encoding': "UTF-8"}
    data = data.set_index(index_columns).round(2)
    cm = sns.diverging_palette(10, 130, as_cmap=True)
    df_html = data.style.apply(_background_gradient, cmap=cm, m=-50, M=50).render()
    imgkit.from_string(df_html, file, options=options)
