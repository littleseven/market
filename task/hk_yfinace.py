# -*- coding:utf-8 -*-

import yfinance as yf
msft = yf.Ticker("0001.HK")
# get stock info
msft.info
# get historical market data
hist = msft.history(period="1y", prepost=True)
# show actions (dividends, splits)
msft.actions
# show dividends
msft.dividends
# show splits
msft.splits
# show financials
msft.financials
msft.quarterly_financials

msft = yf.Ticker("BRK-B")
# get stock info
msft.info
print(msft.info["trailingPE"])
print(msft.info["forwardPE"])
# get historical market data
hist = msft.history(period="1y")
# show actions (dividends, splits)
msft.actions
# show dividends
msft.dividends
# show splits
msft.splits
# show financials
msft.financials
msft.quarterly_financials

