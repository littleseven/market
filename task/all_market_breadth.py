# -*- coding:utf-8 -*-
from task import hk_market_breadth
from task import us_market_breadth
from task import hsc_market_breadth

from task import hk_get_daily
from task import us_get_daily
from task import hsc_get_daily


def get_daily():
    hk_get_daily.get_daily()
    us_get_daily.get_daily()
    hsc_get_daily.get_daily()


def market_breadth():
    hk_market_breadth.market_breadth()
    us_market_breadth.market_breadth()
    hsc_market_breadth.market_breadth()


if __name__ == '__main__':
    get_daily()
    # market_breadth()
