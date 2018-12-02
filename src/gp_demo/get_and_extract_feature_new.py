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
    cal_dates = trade_cal[-11:-1]
    last_cal_date = cal_dates[-1]
    print("cal_dates", cal_dates)

    start = 0
    step = 100
    print("start", start)
    # codes = codes[start * step:start * step + step]

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

        master_df_cols = []
        master_df_data = None
        daily_data_dict = {}
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
                # for each code.
                daily_data = pydash.get(daily_data_dict, code, None)
                if daily_data is None:
                    daily_data = get_daily_data(code, just_download=False)
                    daily_data_dict[code] = daily_data

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

            if df_features is not None:
                if master_df_cols is None:
                    master_df_cols = df_features.columns.tolist()
                if master_df_data is None:
                    master_df_data = df_features.values.tolist()
                else:
                    master_df_data = pydash.concat(master_df_data, df_features.values.tolist())
        # end for code in codes:
        daily_features = pd.DataFrame(master_df_data, columns=master_df_cols)
        daily_features.to_csv(csv_path_daily_features, index=False)
    print("start", start)
