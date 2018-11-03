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
    csv_path_basics = "basics.csv"

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


if __name__ == "__main__":
    codes = get_codes()
    now_date = datetime.now()

    cal_date = pro.trade_cal(exchange_id='', start_date='20180101',
                             end_date='%4d%02d%02d' % (now_date.year, now_date.month, now_date.day))[
        "cal_date"].tolist()

    # code = "000061"
    # daily_data = get_daily_data(code, just_download=False)
    # exit()

    for code in codes:
        daily_data = get_daily_data(code, just_download=False)
        # print("daily_data")
        # print(daily_data)
        for quering_date in cal_date:
            minites_data = get_min_data(code, quering_date=quering_date,just_download=True)
            print("Done", code, quering_date)
