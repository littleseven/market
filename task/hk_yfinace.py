# -*- coding:utf-8 -*-

import yfinance as yf
msft = yf.Ticker("0001.HK")
# get stock info
msft.info
# get historical market data
hist = msft.history(period="max")
# show actions (dividends, splits)
msft.actions
# show dividends
msft.dividends
# show splits
msft.splits
# show financials
msft.financials
msft.quarterly_financials

msft = yf.Ticker("MSFT")
# get stock info
msft.info
# get historical market data
hist = msft.history(period="max")
# show actions (dividends, splits)
msft.actions
# show dividends
msft.dividends
# show splits
msft.splits
# show financials
msft.financials
msft.quarterly_financials