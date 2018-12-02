import os
import time
from datetime import datetime

from feature_tools import do_extract_feature

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
    cal_date = trade_cal[-31:-1]
    last_cal_date = cal_date[-1]
    print("cal_date", cal_date)
    exit()

    all_df_features_values = []
    all_df_features_cols = None
    # codes = [538]
    # codes = pydash.reverse(codes)

    all = list(range(0, 37))
    # [4, 6, 9, 13, 14, 18, 24]
    # all = []
    good = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
            29, 30, 31, 32, 33, 34, 35]
    todo = pydash.difference(all, good)
    print("todo", todo)
    # start = todo[0]
    start = 7
    step = 100
    print("start", start)
    codes = codes[start * step:start * step + step]

    # code = 61
    # quering_date = "2018-11-29"
    # minites_data = get_min_data(code, quering_date=quering_date, is_for_train_not_eval=True,
    #                             just_download=False)
    # print("minites_data", minites_data)
    # exit()
    for idx, code in enumerate(codes):
        csv_path_features = "%s/data_features/data.code_%s.%s.extract_feature.csv" % (
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
                print("Done", idx, code, quering_date, "minites data is None?", minites_data is None)

                if minites_data is not None:
                    if master_df_cols is None:
                        master_df_cols = minites_data.columns.tolist()
                    # minites_data is Dataframe type.
                    master_df_data = pydash.concat(master_df_data, minites_data.values.tolist())

            if pydash.is_empty(master_df_data):
                print("Code %06d's master_df_data is None" % code)
                continue

            master_df = pd.DataFrame(master_df_data, columns=master_df_cols)

            df_features = do_extract_feature(spark, master_df, daily_data, csv_path_features)

    print("start", start)
