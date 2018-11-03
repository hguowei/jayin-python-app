import pandas as pd

import tushare
import pydash
from datetime import datetime
import os
import numpy as np

print(pydash.__version__)


def _get_ymd_from_date_string(date_string):
    if isinstance(date_string, datetime):
        date_string = _to_query_date_string(date_string)

    if pydash.includes(date_string, "-"):
        year = int(date_string[0:4])
        month = int(date_string[5:7])
        day = int(date_string[8:10])
    else:
        year = int(date_string[0:4])
        month = int(date_string[4:6])
        day = int(date_string[6:8])
    # else:
    #     raise Exception("Exception of date '%s'!"% date_string)
    return year, month, day


def _to_query_date_string(date):
    if isinstance(date, str):
        date = _to_query_date(date)
    return "%4d-%02d-%02d" % (date.year, date.month, date.day)


def _to_query_date(date):
    if isinstance(date, str):
        year, month, day = _get_ymd_from_date_string(date)
        return datetime(year=year, month=month, day=day)
    else:
        return datetime(year=date.year, month=date.month, day=date.day)


def query_daily_data(code, start_date_string, end_date_string, ktype="D"):
    print("query_daily_data(", code, ",", start_date_string, ",", end_date_string, ")")
    if isinstance(code, int):
        code = "%06d" % code

    start_date_string = _to_query_date_string(start_date_string)
    end_date_string = _to_query_date_string(end_date_string)

    # print("Quering ", code, " from", start_date_string, " to ", end_date_string)
    data = tushare.get_k_data(code=code,
                              start=start_date_string,
                              end=end_date_string,
                              ktype=ktype)

    if data is None or (isinstance(data, pd.DataFrame) and data.empty):
        return []

    get_end_date_string = data.iloc[-1].date

    year, month, day = _get_ymd_from_date_string(get_end_date_string)
    end_date = datetime(year=year, month=month, day=day)

    def filter(date_value, date_string):
        return pydash.is_equal(date_value, date_string)

    last_day_length = pydash.filter_(data["date"].values, lambda xx: filter(xx, get_end_date_string))

    def is_need_query_again(length):
        is_need_query_daily_data = pydash.is_equal(ktype, "D") and length == 1
        is_need_query_5min_data = pydash.is_equal(ktype, "5") and length == (60 / 5)
        return is_need_query_daily_data or is_need_query_5min_data

    if not is_need_query_again(last_day_length):
        # end date's data is good
        new_start_date = end_date + pd.Timedelta(days=1)
    else:
        new_start_date = end_date

    query_end_date = _to_query_date(end_date_string)
    if new_start_date < query_end_date:
        new_result = query_daily_data(code, new_start_date, query_end_date, ktype)
        if isinstance(new_result, np.ndarray):
            new_result = new_result.tolist()
        if pydash.is_empty(new_result):
            return data.values
        else:
            return pydash.concat(data.values, new_result)
    else:
        return data.values


def get_daily_data(code, start_string="2018-01-01", just_download=False):
    if isinstance(code, int):
        code = "%06d" % code
    now_date = datetime.now()
    ktype = "D"
    _end_string = _to_query_date_string(now_date)
    csv_path = "data/data.%s.%s.csv" % (code, ktype)
    result_data = None

    if just_download and os.path.exists(csv_path):
        return True
    if os.path.exists(csv_path):
        cur_data = pd.read_csv(csv_path)
        if not cur_data.empty:
            start_string = _to_query_date(cur_data.iloc[-1].date) + pd.Timedelta(days=1)
            result_data = cur_data
    else:
        start_string = start_string

    q_data = query_daily_data(code, start_string, _end_string, ktype)

    if q_data is None or \
            (isinstance(q_data, np.ndarray) and pydash.is_empty(q_data.tolist())) or \
            (isinstance(q_data, list) and pydash.is_empty(q_data)):
        return result_data

    if result_data is None or result_data.empty:
        result_data = q_data
    else:
        result_data = np.append(result_data.values, q_data, axis=0)

    print("result_data", result_data)
    dataframe = pd.DataFrame(result_data, columns=["date", "open", "close", "high", "low", "volume", "code"])
    dataframe.to_csv(csv_path, index=False)

    return dataframe


if __name__ == "__main__":
    get_daily_data("000001")
