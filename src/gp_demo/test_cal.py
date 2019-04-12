import os
import time
from datetime import datetime

import joblib
import pandas as pd
import pydash
from tsfresh import extract_features
from tsfresh.feature_extraction import ComprehensiveFCParameters
from tsfresh.utilities.dataframe_functions import impute

from tools.five_minite_data import get_min_data
from utils import get_codes, get_csv_path_feature


def do_extract_feature_before230(master_df, csv_path_features=None):
    if csv_path_features is not None:
        if os.path.exists(csv_path_features):
            return pd.read_csv(csv_path_features)

    master_df["date"] = master_df["date"].apply(pd.Timestamp)

    # Get the time before 2:30
    X_endtime = 14 * 60 + 30

    def filter_before230(date, is_filter_before=True):
        val1 = (date.hour * 60 + date.minute)
        # print("date", date, val1, X_endtime, val1 <= X_endtime)
        before_230 = val1 <= X_endtime
        if is_filter_before:
            return before_230
        else:
            return not before_230

    date_list = master_df["date"].tolist()
    is_choose = pydash.map_(date_list, lambda x: filter_before230(x, True))
    master_df_before_230 = master_df[is_choose]

    def to_day(tmp_date):
        new_date_string = "%4d-%02d-%02d" % (tmp_date.year, tmp_date.month, tmp_date.day)
        return new_date_string

    master_df_before_230_date_strings = pydash.map_(master_df_before_230['date'].tolist(), to_day)

    master_df_before_230.loc[:, 'new_date'] = pd.Series(master_df_before_230_date_strings,
                                                        index=master_df_before_230.index)

    master_df_before_230 = master_df_before_230.drop(['date', 'code'], axis=1)

    extraction_settings = ComprehensiveFCParameters()
    extract_result = extract_features(master_df_before_230,
                                      column_id="new_date",
                                      impute_function=impute,
                                      default_fc_parameters=extraction_settings)

    extract_result = extract_result.dropna()

    return extract_result


def get_model():
    percentage = 0.01
    model_path = "test_model.%.2f.pkl" % percentage
    percentage = 0.02
    model_path2 = "test_model.%.2f.pkl" % percentage

    return joblib.load(model_path), joblib.load(model_path2)


if __name__ == "__main__":
    # !/usr/bin/env python
    # coding: utf-8

    # In[13]:

    start_time = time.time()

    codes = get_codes()
    print("len(codes)", len(codes))
    now_date = datetime.now()

    model, model2 = get_model()
    quering_date = "20181207"

    result_list = []

    # codes = np.random.rand(codes)
    codes = codes[:100]
    # print("codes", codes)
    for idx, code in enumerate(codes):
        csv_path_features = get_csv_path_feature(code, quering_date)
        if os.path.exists(csv_path_features):
            try:
                df_features = pd.read_csv(csv_path_features)
            except Exception as e:
                print("rm", csv_path_features)
                raise e
        else:
            master_df_data = []
            master_df_cols = None
            master_df = get_min_data(code, quering_date=quering_date, is_for_train_not_eval=False,
                                     just_download=False)

            if master_df is None:
                continue

            df_features = do_extract_feature_before230(master_df, csv_path_features)

        # print("df_features", df_features.columns)
        # print(df_features)
        result = model.predict(df_features)
        if result[0] == 1:
            prob = model.predict_proba(df_features)[0][1]
            prob2 = model2.predict_proba(df_features)[0][1]
            tmp = code, quering_date, prob, prob2
            print("code", tmp)
            result_list.append(tmp)

    if len(result_list) > 0:
        df = pd.DataFrame(result_list, columns=["code", "date", "prob_0.01", "prob_0.02"])
        result_csv = "result_%s.csv" % quering_date
        print("result_csv", result_csv)
        df.to_csv(result_csv, index=False)

    for tmp_list in result_list:
        print(tmp_list)
