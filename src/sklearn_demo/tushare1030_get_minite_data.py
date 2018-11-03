import pandas as pd

import tushare
import pydash
from datetime import datetime
import os
import numpy as np

from src.sklearn_demo.daily_data import get_daily_data, _to_query_date_string, _get_ymd_from_date_string, _to_query_date

print(pydash.__version__)


def query_minite_data(code, quering_date, ktype):
    print("query_minite_data(", code, ", ", quering_date, ", ", ktype, ")")
    if isinstance(quering_date, datetime):
        start_date_string = _to_query_date_string(quering_date)
    else:
        start_date_string = quering_date

    print("Quering ", code, " from", start_date_string, start_date_string, ktype)
    data = tushare.get_k_data(code=code,
                              start=start_date_string,
                              end=start_date_string,
                              ktype=ktype)

    data = data[data["date"] == quering_date]

    if data is None or (isinstance(data, pd.DataFrame) and data.empty):
        return []
    else:
        return data


def get_min_data(code, quering_date):
    if isinstance(code, int):
        code = "%06d" % code
    ktype = "5"
    csv_path = "data/data.%s.%s.%s.csv" % (code, ktype, quering_date)
    result_data = None

    if os.path.exists(csv_path):
        cur_data = pd.read_csv(csv_path)
        if not cur_data.empty:
            return cur_data

    query_data = query_minite_data(code, quering_date, ktype)

    if result_data is None:
        result_data = query_data
    else:
        result_data = np.append(result_data, query_data, axis=0)

    dataframe = pd.DataFrame(result_data, columns=["date", "open", "close", "high", "low", "volume", "code"])

    dataframe.to_csv(csv_path, index=False)


if __name__ == "__main__":
    code = "000001"
    start_date_string = "2018-01-02"
    quering_date = start_date_string
    dd = get_min_data(code, quering_date)
    print(dd)
