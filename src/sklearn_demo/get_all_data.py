import tushare as ts
import pydash
import pandas as pd
import os
from datetime import datetime

from src.sklearn_demo.daily_data import get_daily_data
from src.sklearn_demo.five_minite_data import get_min_data

print(pydash.__version__)
pro = ts.pro_api(token="d86106d0d028672c3cad3eba4f1891864b8991e4ac4e6d2833755a4d")


def get_codes():
    csv_path_basics = "data/basics.csv"

    if os.path.exists(csv_path_basics):
        df = pd.read_csv(csv_path_basics)
    else:
        df = pro.stock_basic()
        df.to_csv(csv_path_basics, index=False)

    # print("shape", df.shape)
    # print("df.head()", df.head())
    # print("df.tail()", df.tail())
    # print("df.tail()", df.index)

    return df["symbol"].tolist()


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
