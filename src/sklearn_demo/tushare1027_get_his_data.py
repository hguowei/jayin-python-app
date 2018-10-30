import pandas as pd

import tushare
import pydash
from datetime import datetime
import os
import numpy as np

print(pydash.__version__)

now_date = datetime.now()


def get_ymd_from_date_string(date_string):
    year = int(date_string[0:4])
    month = int(date_string[5:7])
    day = int(date_string[8:10])
    return year, month, day


def to_query_date_string(date):
    return "%4d-%02d-%02d" % (date.year, date.month, date.day)


def to_query_date(date):
    if isinstance(date, str):
        year, month, day = get_ymd_from_date_string(date)
        return datetime(year=year, month=month, day=day)
    else:
        return datetime(year=date.year, month=date.month, day=date.day)


print(get_ymd_from_date_string("2017-01-01"))

end_string = to_query_date_string(now_date)
ktype = "D"


def get_data(code, start_date_string, end_date_string):
    print("get_data(", start_date_string, ", ", end_date_string, ")")
    if isinstance(start_date_string, datetime):
        start_date_string = to_query_date_string(start_date_string)
    if isinstance(end_date_string, datetime):
        end_date_string = to_query_date_string(end_date_string)

    print("Quering from", start_date_string, " to ", end_date_string)
    data = tushare.get_k_data(code=code,
                              start=start_date_string,
                              end=end_date_string,
                              ktype=ktype)
    if data is None or (isinstance(data, pd.DataFrame) and data.empty):
        return []

    # print("data", data)
    get_end_date_string = data.iloc[-1].date
    print("get_end_date_string", get_end_date_string)
    year, month, day = get_ymd_from_date_string(get_end_date_string)
    end_date = datetime(year=year, month=month, day=day)

    print("data", data.shape)
    print("data", data.head())
    print("data", data.tail())

    print("get_end_date_string", get_end_date_string)

    def filter(date_value, date_string):
        return pydash.is_equal(date_value, date_string)

    filter1 = pydash.filter_(data["date"].values, lambda xx: filter(xx, get_end_date_string))
    print('data["date" == get_end_date_string]', filter1)
    print('get_end_date_string', len(filter1))

    if len(filter1) == 1:
        # end date's data is good
        new_start_date = end_date + pd.Timedelta(days=1)
    else:
        new_start_date = end_date

    query_end_date = to_query_date(end_date_string)
    print("new_start_date", new_start_date)
    print("query_end_date", query_end_date)
    if new_start_date < query_end_date:
        print("Xxxxxxxx")
        return pydash.concat(data.values, get_data(code, new_start_date, query_end_date))
    else:
        return data.values


def get_his_data(code, start_string="2018-01-01"):
    csv_path = "data/data.%s.%s.csv" % (code, ktype)
    result_data = None

    if os.path.exists(csv_path):
        cur_data = pd.read_csv(csv_path)
        if not cur_data.empty:
            start_string = to_query_date(cur_data.iloc[-1].date) + pd.Timedelta(days=1)
            result_data = cur_data.values
    else:
        start_string = start_string

    query_data = get_data(code, start_string, end_string)
    if result_data is None:
        result_data = query_data
    else:
        result_data = np.append(result_data, query_data, axis=0)

    dataframe = pd.DataFrame(result_data, columns=["date", "open", "close", "high", "low", "volume", "code"])

    dataframe.to_csv(csv_path, index=False)


get_his_data("000001")
exit()
