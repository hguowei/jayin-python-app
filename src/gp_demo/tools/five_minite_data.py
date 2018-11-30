import os
from datetime import datetime

import pandas as pd
import pydash
import tushare

from src.gp_demo import dataset_base_dir
from tools.daily_data import to_query_daily_data, to_query_date

print(pydash.__version__)


def get_minite_csv_path(code, ktype, quering_date):
    return "%s/data/data.%s.%s.%s.csv" % (dataset_base_dir, code, ktype, quering_date)


def get_query_data(data, query_date):
    def is_query_date(data):
        tmp_date_list = data["date"].tolist()

        def map_func(tmp_date):
            is_equal = pydash.is_equal(to_query_date(tmp_date), query_date)
            # print("tmp", tmp_date, quering_date, is_equal)
            return is_equal

        return pydash.chain(tmp_date_list).map(map_func).value()

    return data[is_query_date(data)]


def query_minite_data(code, query_date, ktype, is_print=True, is_saving_others=True):
    '''
    :param code:
    :param query_date:
    :param ktype: = 5
    :param is_print:
    :return: python list type.
    '''
    if is_print:
        print("query_minite_data(", code, ", ", query_date, ", ", ktype, ")")

    if isinstance(query_date, datetime):
        start_date_string = to_query_date(query_date)
    else:
        start_date_string = query_date

    minite_csv_path = get_minite_csv_path(code, ktype, start_date_string)

    # print("Quering ", code, " from", start_date_string, start_date_string, ktype)
    data = tushare.get_k_data(code=code,
                              start=start_date_string,
                              end=start_date_string,
                              ktype=ktype)

    result = pydash.chain(data["date"].tolist()).group_by(lambda d: d).values().map(
        lambda key: (key[0], len(key))).value()
    for tmp_date, count in result:
        if is_saving_others and count == int(4 * 60 / 5):
            print("tmp_date", tmp_date)
            get_query_data(data, tmp_date).to_csv(minite_csv_path, index=False)

    data = get_query_data(data, query_date)
    if data is None or (isinstance(data, pd.DataFrame) and data.empty):
        return None
    else:
        return data


def get_min_data(code, quering_date, is_for_train_not_eval=True, just_download=False):
    '''
    :param code:
    :param quering_date:
    :param is_for_train_not_eval: train data must has length = 4 * 60 / 5, eval data length = 3.5 * 60 / 5
    :param just_download:
    :return: Dataframe type, columns=["date", "open", "close", "high", "low", "volume", "code"]
    '''
    ktype = "5"
    if isinstance(code, int):
        code = "%06d" % code

    if quering_date is None:
        return tushare.get_k_data(code=code,
                                  ktype=ktype)

    if len(quering_date) == 8:
        quering_date = to_query_date(quering_date)
    csv_path = get_minite_csv_path(code, ktype, quering_date)

    if just_download and os.path.exists(csv_path):
        return True

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

    if os.path.exists(csv_path):
        tmp_csv_data = pd.read_csv(csv_path)
        if is_can_return(tmp_csv_data):
            return tmp_csv_data

    query_data = query_minite_data(code, quering_date, ktype)

    if query_data is None or query_data.empty:
        return None

    if just_download and is_can_return(query_data):
        return None

    dataframe = pd.DataFrame(query_data, columns=["date", "open", "close", "high", "low", "volume", "code"])

    dataframe.to_csv(csv_path, index=False)
    return dataframe


if __name__ == "__main__":
    date_list = ["a", "b", "a"]
    result = pydash.chain(date_list).group_by(lambda d: d).values().map(lambda key: (key[0], len(key))).value()
    print("result", dict(result))
    exit()
    for key in result.keys():
        result[key] = len(result[key])
    print("result", result)
    exit()
    code = "000001"
    start_date_string = "2018-01-02"
    quering_date1 = start_date_string
    dd = get_min_data(code, quering_date1)
    print(dd)
