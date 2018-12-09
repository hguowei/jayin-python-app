import os
import time
from datetime import datetime

import pandas as pd
import pydash
import tushare as ts
from pyspark.sql import SparkSession
from tsfresh import extract_features
from tsfresh.feature_extraction import ComprehensiveFCParameters
from tsfresh.utilities.dataframe_functions import impute

from src.gp_demo import dataset_base_dir, csv_path_basics, pro
from src.sklearn_demo.daily_data import get_daily_data
from src.sklearn_demo.five_minite_data import get_min_data
from src.sklearn_demo.get_all_data import get_trade_cal_list
import joblib


def get_codes():
    if os.path.exists(csv_path_basics):
        df = pd.read_csv(csv_path_basics)
    else:
        df = pro.stock_basic()
        df.to_csv(csv_path_basics, index=False)

    # print("shape", df.shape)
    # print("df.head()", df.head())
    # print("df.tail()", df.tail())
    # print("df.tail()", df.index)

    return df["symbol"].tolist()


def get_train_data_csv_path(last_cal_date):
    return "%s/data_to_train/data.%s.to_train.csv" % (dataset_base_dir, last_cal_date)


def get_csv_path_feature(code, quering_date):
    csv_path_features = "%s/code_daily_features/code_%s.date_%s.features.csv" % (
        dataset_base_dir, code, quering_date)
    return csv_path_features


def get_model():
    percentage = 0.01
    model_path = "test_model.%.2f.pkl" % percentage
    percentage = 0.02
    model_path2 = "test_model.%.2f.pkl" % percentage

    return joblib.load(model_path), joblib.load(model_path2)
