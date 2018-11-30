import tushare as ts
import pydash
import pandas as pd
import os
from datetime import datetime

import time
import pandas as pd
from pyspark.sql import SparkSession
from tsfresh import extract_features
from tsfresh.feature_extraction import ComprehensiveFCParameters
from tsfresh.utilities.dataframe_functions import impute
import pydash

from tools.get_all_data import get_trade_cal_list
from utils import get_codes

print(pydash.__version__)


def get_ymd_from_date_string(date_string):
    year = int(date_string[0:4])
    month = int(date_string[5:7])
    day = int(date_string[8:10])
    return year, month, day


def to_query_date(date):
    if isinstance(date, str):
        year, month, day = get_ymd_from_date_string(date)
        return datetime(year=year, month=month, day=day)
    else:
        return datetime(year=date.year, month=date.month, day=date.day)



def do_extract_feature(spark, master_df, df_day, csv_path_features=None):
    if csv_path_features is not None:
        if os.path.exists(csv_path_features):
            return pd.read_csv(csv_path_features)

    day_open_dict = dict(pydash.chain(df_day["date"].tolist()).zip(df_day["open"].tolist()).value())

    first_date = pd.Timestamp(master_df["date"][0]) + pd.offsets.Hour(7)

    master_df["date"] = master_df["date"].apply(pd.Timestamp)
    master_df = master_df[master_df["date"].apply(pd.Timestamp) > first_date]

    # Get the time before 2:30
    X_endtime = 14 * 60 + 30

    def filter_before230(row, is_filter_before=True):
        date = row.date
        # val1 = (date.hour * 60 + date.minute)
        # print("date", date, val1, X_endtime, val1 <= X_endtime)
        before_230 = (date.hour * 60 + date.minute) <= X_endtime
        if is_filter_before:
            return before_230
        else:
            return not before_230

        # return date.hour == 14

    # print("master_df")
    # print(master_df)
    master_df_before_230 = master_df[master_df.apply(lambda row: filter_before230(row, True), axis=1)]
    master_df_after_230 = master_df[master_df.apply(lambda row: filter_before230(row, False), axis=1)]

    # print("master_df_before_230", master_df_before_230.head())
    # print("master_df_after_230", master_df_after_230.head())

    def to_day(tmp_date):
        new_date_string = "%4d-%02d-%02d" % (tmp_date.year, tmp_date.month, tmp_date.day)
        return new_date_string

    master_df_before_230_date_strings = pydash.map_(master_df_before_230['date'].tolist(), to_day)

    master_df_before_230.loc[:, 'new_date'] = pd.Series(master_df_before_230_date_strings,
                                                        index=master_df_before_230.index)

    master_df_before_230 = master_df_before_230.drop(['date', 'code'], axis=1)

    def map_func(kv):
        tmp_date = kv[0]
        row_list = kv[1]
        import pydash

        new_date_string = "%4d-%02d-%02d" % (tmp_date.year, tmp_date.month, tmp_date.day)
        next_day_open = pydash.get(day_open_dict, new_date_string, 0)

        if next_day_open > 0:
            max_value = pydash.chain(row_list).map(lambda row: row.close).max().value()
            return [[new_date_string, (max_value - next_day_open) / next_day_open]]
        else:
            return []

    def to_kv_func(row):
        from datetime import datetime
        tmp_date = row.date
        new_date = datetime(tmp_date.year, tmp_date.month, tmp_date.day)
        return new_date, row

    max_can_buy = spark.createDataFrame(master_df_after_230).rdd.map(to_kv_func).groupByKey().flatMap(
        map_func).collect()

    date_list = pydash.map_(max_can_buy, lambda kv: kv[0])
    value_list = pydash.map_(max_can_buy, lambda kv: kv[1])

    result = pd.Series(value_list, index=date_list)

    extraction_settings = ComprehensiveFCParameters()
    extract_result = extract_features(master_df_before_230,
                                      column_id="new_date",
                                      impute_function=impute,
                                      default_fc_parameters=extraction_settings)

    extract_result["label"] = result
    extract_result = extract_result.dropna()

    extract_result.to_csv(csv_path_features, index=False)


if __name__ == "__main__":
    # !/usr/bin/env python
    # coding: utf-8

    # In[13]:

    start_time = time.time()

    spark = SparkSession.builder \
        .master("local") \
        .appName("Word Count") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()

    codes = get_codes()
    print("len(codes)", len(codes))
    now_date = datetime.now()

    trade_cal = get_trade_cal_list(now_date)
    print("trade_cal", trade_cal)
    cal_date = trade_cal[-31:-1]
    # cal_date = trade_cal[-1:]
    print("cal_date", cal_date)

    last_cal_date = cal_date[-1]

    all_df_features_values = []
    all_df_features_cols = None

    codes = codes[-1:]
    for idx, code in enumerate(codes):
        csv_path_features = "%s/data_merge_result/data.%s.%s.result.csv" % (dataset_base_dir, code, last_cal_date)
        daily_data = get_daily_data(code, just_download=False)
        if daily_data is None:
            continue
        print("daily_datadaily_datadaily_datadaily_data")
        master_df_data = []
        master_df_cols = None

        quering_date = None
        try:
            # None is all.
            minites_data = get_min_data(code, quering_date=quering_date, is_for_train_not_eval=False,
                                        just_download=False)
        except:
            minites_data = None
        print("Done", idx, code, quering_date, "minites data is None?", minites_data is None)

        if minites_data is not None and isinstance(minites_data, pd.DataFrame) and master_df_cols is None:
            master_df_cols = minites_data.columns.tolist()

        get_end_date_string = minites_data.iloc[-1].date
        get_end_date_string = get_end_date_string[0:10]
        print("get_end_date_string", get_end_date_string)


        def filter_func(row, date_string):
            date_value = row.date
            return pydash.starts_with(date_value, date_string)


        print("minites_data", type(minites_data), minites_data)
        # Get last day data.
        minites_data = minites_data[minites_data.apply(lambda row: filter_func(row, get_end_date_string), axis=1)]
        print('data["date" == get_end_date_string]', minites_data)
        print('get_end_date_string', len(minites_data))

        X_endtime = 14 * 60 + 30


        def filter_before230(row, is_filter_before=True):
            date = pd.Timestamp(row.date)
            # val1 = (date.hour * 60 + date.minute)
            # print("date", date, val1, X_endtime, val1 <= X_endtime)
            before_230 = (date.hour * 60 + date.minute) <= X_endtime
            if is_filter_before:
                return before_230
            else:
                return not before_230


        # just filter data before 2:30
        # minites_data = pydash.filter_(minites_data, lambda row: filter_before230(row, True))
        minites_data = minites_data[minites_data.apply(lambda row: filter_before230(row, True), axis=1)]

        print("before_230", len(minites_data), minites_data)


        def get_df_or_list_values(xxx):
            if isinstance(xxx, pd.DataFrame):
                return xxx.values.tolist()
            else:
                return xxx


        if minites_data is not None:
            master_df_data = pydash.concat(master_df_data, get_df_or_list_values(minites_data))

        if pydash.is_empty(master_df_data):
            continue

        print("master_df_data", master_df_data)
        print("master_df_cols", master_df_cols)
        master_df = pd.DataFrame(master_df_data, columns=master_df_cols)

        if len(master_df) < int(60 / 5 * 3.5):
            print("CCCCCCCC")
            continue
        df_features = do_extract_feature(spark, master_df, daily_data, csv_path_features)

        print("len", len(df_features))
        exit()
        continue
        # if df_features is None:
        #     continue
        # else:
        #     all_df_features_values = pydash.concat(all_df_features_values, df_features.values.tolist())
        #
        # if all_df_features_cols is None:
        #     all_df_features_cols = df_features.columns.tolist()

