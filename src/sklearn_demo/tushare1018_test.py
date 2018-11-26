#!/usr/bin/python
# coding: UTF-8

"""This script parse stock info"""

import tushare as ts


def parse(STOCK):
    '''process stock'''
    is_buy = 0
    buy_val = []
    buy_date = []
    sell_val = []
    sell_date = []
    df = None# ts.get_hist_data(STOCK)
    ma20 = df[u'ma20']
    close = df[u'close']
    rate = 1.0
    idx = len(ma20)

    while idx > 0:
        idx -= 1
        close_val = close[idx]
        ma20_val = ma20[idx]
        if close_val > ma20_val:
            if is_buy == 0:
                is_buy = 1
                buy_val.append(close_val)
                buy_date.append(close.keys()[idx])
        elif close_val < ma20_val:
            if is_buy == 1:
                is_buy = 0
                sell_val.append(close_val)
                sell_date.append(close.keys()[idx])

    print("stock number: %s" % STOCK)
    print("buy count   : %d" % len(buy_val))
    print("sell count  : %d" % len(sell_val))

    for i in range(len(sell_val)):
        rate = rate * (sell_val[i] * (1 - 0.002) / buy_val[i])
        print("buy date : %s, buy price : %.2f" % (buy_date[i], buy_val[i]))
        print("sell date: %s, sell price: %.2f" % (sell_date[i], sell_val[i]))

    print("rate: %.2f" % rate)


if __name__ == '__main__':
    STOCK = '600000'  ##浦发银行
    parse(STOCK)

# stock number: 600000
# buy count   : 37
# sell count  : 37
# buy date : 2016-04-20, buy price : 17.98
# sell date: 2016-04-25, sell price: 17.88
# buy date : 2016-05-03, buy price : 18.14
# sell date: 2016-05-06, sell price: 17.74
# buy date : 2016-05-25, buy price : 17.67
# sell date: 2016-06-15, sell price: 17.76
# buy date : 2016-06-20, buy price : 17.86
# sell date: 2016-06-21, sell price: 17.81
# buy date : 2016-07-20, buy price : 15.75
# sell date: 2016-07-22, sell price: 15.61
# buy date : 2016-07-25, buy price : 15.69
# sell date: 2016-07-29, sell price: 15.69
# buy date : 2016-08-01, buy price : 15.80
# sell date: 2016-08-03, sell price: 15.67
# buy date : 2016-08-05, buy price : 15.72
# sell date: 2016-09-12, sell price: 16.40
# buy date : 2016-09-13, buy price : 16.45
# sell date: 2016-09-14, sell price: 16.40
# buy date : 2016-09-19, buy price : 16.47
# sell date: 2016-10-13, sell price: 16.43
# buy date : 2016-10-24, buy price : 16.47
# sell date: 2016-10-25, sell price: 16.42
# buy date : 2016-11-04, buy price : 16.39
# sell date: 2016-12-15, sell price: 16.70
# buy date : 2017-01-13, buy price : 16.27
# sell date: 2017-02-17, sell price: 16.64
# buy date : 2017-02-20, buy price : 16.91
# sell date: 2017-02-23, sell price: 16.69
# buy date : 2017-04-05, buy price : 16.16
# sell date: 2017-04-10, sell price: 15.97
# buy date : 2017-05-12, buy price : 15.21
# sell date: 2017-05-18, sell price: 15.01
# buy date : 2017-05-22, buy price : 15.04
# sell date: 2017-05-25, sell price: 12.93
# buy date : 2017-06-27, buy price : 12.70
# sell date: 2017-07-03, sell price: 12.56
# buy date : 2017-07-05, buy price : 12.62
# sell date: 2017-07-10, sell price: 12.53
# buy date : 2017-07-11, buy price : 12.80
# sell date: 2017-08-03, sell price: 13.08
# buy date : 2017-08-28, buy price : 12.89
# sell date: 2017-09-21, sell price: 12.87
# buy date : 2017-09-25, buy price : 12.94
# sell date: 2017-09-26, sell price: 12.86
# buy date : 2017-10-09, buy price : 13.04
# sell date: 2017-10-23, sell price: 12.84
# buy date : 2017-11-13, buy price : 12.81
# sell date: 2017-11-14, sell price: 12.60
# buy date : 2017-11-17, buy price : 12.78
# sell date: 2017-12-12, sell price: 12.75
# buy date : 2018-01-09, buy price : 12.71
# sell date: 2018-01-22, sell price: 12.78
# buy date : 2018-01-23, buy price : 12.90
# sell date: 2018-02-08, sell price: 13.10
# buy date : 2018-04-19, buy price : 11.78
# sell date: 2018-04-20, sell price: 11.61
# buy date : 2018-04-24, buy price : 11.78
# sell date: 2018-04-26, sell price: 11.55
# buy date : 2018-07-18, buy price : 9.52
# sell date: 2018-08-15, sell price: 9.91
# buy date : 2018-08-16, buy price : 10.06
# sell date: 2018-08-17, sell price: 9.97
# buy date : 2018-08-20, buy price : 10.15
# sell date: 2018-09-05, sell price: 10.12
# buy date : 2018-09-07, buy price : 10.19
# sell date: 2018-09-11, sell price: 10.02
# buy date : 2018-09-13, buy price : 10.29
# sell date: 2018-09-17, sell price: 10.15
# buy date : 2018-09-18, buy price : 10.26
# sell date: 2018-09-20, sell price: 10.22
# buy date : 2018-09-21, buy price : 10.49
# sell date: 2018-10-08, sell price: 10.16
# buy date : 2018-10-17, buy price : 10.29
# sell date: 2018-10-18, sell price: 10.19
# rate: 0.72
