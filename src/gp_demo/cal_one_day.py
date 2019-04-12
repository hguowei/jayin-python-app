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
from utils import get_codes, get_csv_path_feature, get_model

if __name__ == "__main__":
    start_time = time.time()

    spark = SparkSession.builder \
        .master("local") \
        .appName("Word Count") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()

    codes = get_codes()
    print("len(codes)", len(codes))
    now_date = datetime.now()

    print("codes", len(codes), codes)

    quering_date = "20181212"
    model, model2 = get_model()
    result_list = []

    inner_start_time = time.time()
    # codes = codes[:100]
    codes = pydash.filter_(codes, lambda code: code >= 300000 and code <= 399999)

    # 17 - 23?
    start = 26
    step = 100
    print("start", start)
    codes = codes[start * step:start * step + step]
    for code in codes:
        print("code", code)
        # csv_path_features = "%s/code_daily_features/code_%s.date_%s.features.csv" % (
        #     dataset_base_dir, code, quering_date)
        csv_path_features = get_csv_path_feature(code, quering_date)
        if os.path.exists(csv_path_features):
            try:
                df_features = pd.read_csv(csv_path_features)
            except Exception as e:
                print("rm", csv_path_features)
                raise e
        else:
            try:
                minites_data = get_min_data(code, quering_date=quering_date, is_for_train_not_eval=True,
                                            just_download=False)
            except:
                minites_data = None
            # print("Done", quering_date, code, "minites data is None?", minites_data is None)

            if minites_data is None or (isinstance(minites_data, pd.DataFrame) and minites_data.empty):
                continue
            df_features = do_extract_feature(spark, minites_data)

        # print("df_features", df_features.columns)
        # print(df_features)
        if df_features is None or len(df_features) == 0:
            continue

        to_drop = pydash.intersection(["id", "label"], df_features.columns.tolist())
        df_features.drop(to_drop, axis=1, inplace=True)
        # df_features.fillna(0)
        result = model.predict(df_features)
        if result[0] == 1:
            prob = model.predict_proba(df_features)[0][1]
            prob2 = model2.predict_proba(df_features)[0][1]
            tmp = code, quering_date, prob, prob2
            print("\n\n\n\nPredicted: ", tmp)
            result_list.append(tmp)

    if len(result_list) > 0:
        df = pd.DataFrame(result_list, columns=["code", "date", "prob_0.01", "prob_0.02"])
        result_csv = "result_%s.%d.csv" % (quering_date, start)
        print("result_csv", result_csv)
        df.to_csv(result_csv, index=False)
    else:
        print("NONENONENONENONENONENONENONENONE")

    for tmp_list in result_list:
        print(tmp_list)
