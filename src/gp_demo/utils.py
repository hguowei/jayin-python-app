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
    return "%s/gp_data/data.%s.to_train.csv" % (dataset_base_dir, last_cal_date)