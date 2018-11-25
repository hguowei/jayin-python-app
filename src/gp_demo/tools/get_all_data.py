import tushare as ts
import pydash
import pandas as pd
import os
from datetime import datetime

from src.gp_demo import pro
from tools.daily_data import get_daily_data
from tools.five_minite_data import get_min_data
from utils import get_codes

print(pydash.__version__)


def get_trade_cal_list(now_date):
    try:
        trade_cal = pro.trade_cal(exchange_id='', start_date='20181001',
                                  end_date='%4d%02d%02d' % (now_date.year, now_date.month, now_date.day))[
            "cal_date"].tolist()
    except:
        end_date = '%4d%02d%02d' % (now_date.year, now_date.month, now_date.day)
        trade_cal = list(range(20181001, int(end_date)))

    return trade_cal


if __name__ == "__main__":
    codes = get_codes()
    now_date = datetime.now()

    trade_cal = pro.trade_cal(exchange_id='', start_date='20180101',
                              end_date='%4d%02d%02d' % (now_date.year, now_date.month, now_date.day))[
        "cal_date"]
    cal_date = trade_cal.tolist()[-1:]

    # print(codes)
    # code = "000061"
    # daily_data = get_daily_data(code, just_download=False)
    # exit()

    min_data = []
    for code in codes:
        daily_data = get_daily_data(code, just_download=True)
        # print("daily_data")
        # print(daily_data)
        for quering_date in cal_date:
            minites_data = get_min_data(code, quering_date=quering_date, just_download=True)
            print("Done", code, quering_date)
