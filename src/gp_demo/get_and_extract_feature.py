import os
import time
from datetime import datetime

import pandas as pd
import pydash
from pyspark.sql import SparkSession
from tsfresh import extract_features
from tsfresh.feature_extraction import ComprehensiveFCParameters
from tsfresh.utilities.dataframe_functions import impute

from src.gp_demo import dataset_base_dir
from tools.daily_data import get_daily_data
from tools.five_minite_data import get_min_data
from tools.get_all_data import get_trade_cal_list
from utils import get_codes, get_train_data_csv_path


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
    cal_date = trade_cal[-31:-1]
    last_cal_date = cal_date[-1]

    all_df_features_values = []
    all_df_features_cols = None
    # codes = [538]
    # codes = pydash.reverse(codes)

    all = list(range(0, 35))
    # [4, 6, 9, 13, 14, 18, 24]
    all = [4, 9, 24]
    all = [24]
    good = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31,
            32, 33, 34, 35]
    todo = pydash.difference(all, good)
    print("todo", todo)

    start = todo[0]
    start = 38
    step = 100
    print("start", start)
    # codes = codes[start * step:start * step + step]

    for idx, code in enumerate(codes):
        csv_path_features = "%s/data_train/data.code_%s.%s.extract_feature.csv" % (
            dataset_base_dir, code, last_cal_date)
        if os.path.exists(csv_path_features):
            try:
                df_features = pd.read_csv(csv_path_features)
            except Exception as e:
                print("rm", csv_path_features)
                raise e
        else:
            daily_data = get_daily_data(code, just_download=False)
            if daily_data is None:
                continue
            master_df_data = []
            master_df_cols = None
            for quering_date in cal_date:
                try:
                    minites_data = get_min_data(code, quering_date=quering_date, is_for_train_not_eval=True,
                                                just_download=False)
                except:
                    minites_data = None
                # print("Done", idx, code, quering_date, "minites data is None?", minites_data is None)

                if minites_data is not None:
                    if master_df_cols is None:
                        master_df_cols = minites_data.columns.tolist()
                    # minites_data is Dataframe type.
                    master_df_data = pydash.concat(master_df_data, minites_data.values.tolist())

            if pydash.is_empty(master_df_data):
                continue

            master_df = pd.DataFrame(master_df_data, columns=master_df_cols)

            df_features = do_extract_feature(spark, master_df, daily_data, csv_path_features)

        all_df_features_values.append(df_features)

    print("start", start)
    exit()
    csv_path_to_train = get_train_data_csv_path(last_cal_date)
    to_train_df = pd.DataFrame(all_df_features_values, columns=all_df_features_cols)
    to_train_df.to_csv(csv_path_to_train, index=False)
