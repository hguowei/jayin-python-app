import os
import time
from datetime import datetime

from tools.feature_tools import do_extract_feature

os.environ["PYSPARK_PYTHON"] = "/Users/huang/anaconda2/envs/py36/bin/python"

import pandas as pd
import pydash
from pyspark.sql import SparkSession

from src.gp_demo import dataset_base_dir
from tools.daily_data import get_daily_data
from tools.five_minite_data import get_min_data
from tools.get_all_data import get_trade_cal_list
from utils import get_codes

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

    trade_cal = get_trade_cal_list()
    cal_dates = trade_cal[-13:-1]
    last_cal_date = cal_dates[-1]
    print("cal_dates", cal_dates)

    all_df_features_values = []
    all_df_features_cols = None
    # codes = [538]
    # codes = pydash.reverse(codes)

    all = list(range(0, 37))
    # [4, 6, 9, 13, 14, 18, 24]
    # all = []
    good = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
            29, 30, 31, 32, 33, 34, 35]
    todo_list = pydash.difference(all, good)
    print("todo_list", todo_list)
    # start = todo_list[0]
    start = 5
    step = 100
    print("start", start)
    codes = codes[start * step:start * step + step]

    # cal_dates = [20181116]
    # codes = [1]
    for quering_date in cal_dates:
        csv_path_daily_features = "%s/daily_all_features/date_%s.all_features.csv" % (
            dataset_base_dir, quering_date)

        if os.path.exists(csv_path_daily_features):
            try:
                daily_features = pd.read_csv(csv_path_daily_features)
            except Exception as e:
                print("rm", csv_path_daily_features)
                raise e

        daily_data = None
        for code in codes:
            csv_path_features = "%s/code_daily_features/code_%s.date_%s.features.csv" % (
                dataset_base_dir, code, quering_date)
            if os.path.exists(csv_path_features):
                try:
                    df_features = pd.read_csv(csv_path_features)
                except Exception as e:
                    print("rm", csv_path_features)
                    raise e
            else:
                if daily_data is None:
                    # for each code.
                    daily_data = get_daily_data(code, just_download=False)

                if daily_data is None:
                    print("ERROR, cannot get daily data of code='%s'!" % code)
                    continue
                try:
                    minites_data = get_min_data(code, quering_date=quering_date, is_for_train_not_eval=True,
                                                just_download=False)
                except:
                    minites_data = None
                print("Done", quering_date, code, "minites data is None?", minites_data is None)

                if minites_data is None or (isinstance(minites_data, pd.DataFrame) and minites_data.empty):
                    continue
                df_features = do_extract_feature(spark, minites_data, daily_data, csv_path_features)

    print("start", start)
