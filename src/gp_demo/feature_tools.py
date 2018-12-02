import os

os.environ["PYSPARK_PYTHON"] = "/Users/huang/anaconda2/envs/py36/bin/python"

import pandas as pd
import pydash
from tsfresh import extract_features
from tsfresh.feature_extraction import ComprehensiveFCParameters
from tsfresh.utilities.dataframe_functions import impute


def do_extract_feature(spark, master_df, df_day, csv_path_features=None):
    if csv_path_features is not None:
        if os.path.exists(csv_path_features):
            return pd.read_csv(csv_path_features)

    master_df["date"] = master_df["date"].apply(pd.Timestamp)

    def code_to_string(code):
        if isinstance(code, int):
            return "%06d" % code
        else:
            return code

    master_df["code"] = master_df["code"].apply(code_to_string)

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
    # print("date_list", date_list)

    is_before = pydash.map_(date_list, lambda x: filter_before230(x, True))
    master_df_before_230 = master_df[is_before]
    is_after = pydash.map_(date_list, lambda x: filter_before230(x, False))
    master_df_after_230 = master_df[is_after]
    # print("master_df_after_230")
    # print(master_df_after_230)

    trade_day_list = df_day["date"].tolist()
    trade_day_open = df_day["open"].tolist()
    next_day_open_dict = dict(zip(trade_day_list[:-1], trade_day_open[1:]))
    # print("next_day_open_dict", next_day_open_dict)

    # Get the time before 2:30
    X_endtime = 14 * 60 + 30

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
        next_day_open = pydash.get(next_day_open_dict, new_date_string, 0)

        if next_day_open > 0:
            max_value = pydash.chain(row_list).map(lambda row: row.close).max().value()
            # print("row_list", list(row_list))
            # print("max_value", max_value)
            return [[new_date_string, (next_day_open - max_value) / max_value]]
        else:
            return []

    def to_kv_func(row):
        from datetime import datetime
        tmp_date = row.date
        new_date = datetime(tmp_date.year, tmp_date.month, tmp_date.day)
        return new_date, row

    # print("master_df_after_230", master_df_after_230)
    x1 = spark.createDataFrame(master_df_after_230)
    rdd1 = x1.rdd.map(to_kv_func)
    # print("rdd1", rdd1.take(1))
    rdd2 = rdd1.groupByKey()
    # print("rdd2", rdd2.take(1))
    max_can_buy = rdd2.flatMap(
        map_func).collect()
    # print("max_can_buy", max_can_buy)
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

    if csv_path_features is not None:
        extract_result.to_csv(csv_path_features, index=False)

    return extract_result
