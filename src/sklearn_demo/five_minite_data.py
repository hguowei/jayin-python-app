import pandas as pd

import tushare
import pydash
from datetime import datetime
import os
import numpy as np

from src.sklearn_demo.daily_data import get_daily_data, _to_query_date_string, _get_ymd_from_date_string, _to_query_date

print(pydash.__version__)


def query_minite_data(code, quering_date, ktype, is_print=False):
    if is_print:
        print("query_minite_data(", code, ", ", quering_date, ", ", ktype, ")")
    if isinstance(quering_date, datetime):
        start_date_string = _to_query_date_string(quering_date)
    else:
        start_date_string = quering_date

    # print("Quering ", code, " from", start_date_string, start_date_string, ktype)
    data = tushare.get_k_data(code=code,
                              start=start_date_string,
                              end=start_date_string,
                              ktype=ktype)

    def is_query_date(data):
        tmp_date_list = data["date"].tolist()

        def map_func(tmp_date):
            is_equal = pydash.is_equal(_to_query_date_string(tmp_date), quering_date)
            # print("tmp", tmp_date, quering_date, is_equal)
            return is_equal

        return pydash.chain(tmp_date_list).map(map_func).value()

    data = data[is_query_date(data)]

    if data is None or (isinstance(data, pd.DataFrame) and data.empty):
        return []
    else:
        return data


def get_min_data(code, quering_date, is_for_train_not_eval=True, just_download=False):
    if isinstance(code, int):
        code = "%06d" % code

    if len(quering_date) == 8:
        quering_date = _to_query_date_string(quering_date)
    ktype = "5"
    csv_path = "data/data.%s.%s.%s.csv" % (code, ktype, quering_date)
    result_data = None

    def is_can_return(result_data):
        if is_for_train_not_eval:
            if len(result_data) < 4 * 12:
                if os.path.exists(csv_path):
                    os.remove(csv_path)
                return True
        else:
            if len(result_data) < int(3.5 * 12):
                if os.path.exists(csv_path):
                    os.remove(csv_path)
                return True
        return True

    if just_download and os.path.exists(csv_path):
        return True
    if os.path.exists(csv_path):
        tmp_csv_data = pd.read_csv(csv_path)
        if is_can_return(tmp_csv_data):
            return tmp_csv_data

    query_data = query_minite_data(code, quering_date, ktype)

    if result_data is None:
        result_data = query_data
    else:
        result_data = np.append(result_data, query_data, axis=0)

    if is_can_return(result_data):
        return None
    dataframe = pd.DataFrame(result_data, columns=["date", "open", "close", "high", "low", "volume", "code"])

    dataframe.to_csv(csv_path, index=False)


if __name__ == "__main__":
    code = "000001"
    start_date_string = "2018-01-02"
    quering_date = start_date_string
    dd = get_min_data(code, quering_date)
    print(dd)
