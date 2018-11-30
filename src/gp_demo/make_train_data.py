import os
import time
from datetime import datetime

import pandas as pd
from pyspark.sql import SparkSession

from src.gp_demo import dataset_base_dir
from tools.get_all_data import get_trade_cal_list
from utils import get_codes, get_train_data_csv_path

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

    idx = 0
    for code in codes:
        idx += 1
        csv_path_features = "%s/data_train/data.code_%s.%s.extract_feature.csv" % (
            dataset_base_dir, code, last_cal_date)
        if os.path.exists(csv_path_features):
            try:
                df_features = pd.read_csv(csv_path_features)
            except Exception as e:
                print("rm", csv_path_features)
                raise e
        else:
            continue
        if all_df_features_cols is None:
            all_df_features_cols = df_features.columns.tolist()
        all_df_features_values.extend(df_features.values.tolist())
        if idx % 10 == 500 and idx > 490:
            csv_path = "%s/gp_data/data.%s.to_train.ckpt_%d.csv" % (dataset_base_dir, last_cal_date, idx)
            tmp_df = pd.DataFrame(all_df_features_values, columns=all_df_features_cols)
            print("Saving checkpoint to '%s'!" % csv_path)
            tmp_df.to_csv(csv_path, index=False)

    csv_path_to_train = get_train_data_csv_path(last_cal_date)
    to_train_df = pd.DataFrame(all_df_features_values, columns=all_df_features_cols)
    print("Saving to '%s'!" % csv_path_to_train)
    to_train_df.to_csv(csv_path_to_train, index=False)
