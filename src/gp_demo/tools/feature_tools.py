import os

from src.gp_demo import dataset_base_dir

os.environ["PYSPARK_PYTHON"] = "/Users/huang/anaconda2/envs/py36/bin/python"

import pandas as pd
import pydash
from tsfresh import extract_features
from tsfresh.feature_extraction import ComprehensiveFCParameters
from tsfresh.utilities.dataframe_functions import impute


def do_extract_feature(spark, master_df, df_day=None, csv_path_features=None):
    if csv_path_features is not None:
        if os.path.exists(csv_path_features):
            return pd.read_csv(csv_path_features)

    # print("master_df", master_df)
    # print("df_day", df_day)
    master_df["date"] = master_df["date"].apply(pd.Timestamp)

    def code_to_string(code):
        if isinstance(code, int):
            return "%06d" % code
        else:
            return code

    master_df["code"] = master_df["code"].apply(code_to_string)

    # Get the time before 2:30
    X_endtime = 14 * 60 + 30

    def filter_before230(date):
        val1 = (date.hour * 60 + date.minute)
        # print("date", date, val1, X_endtime, val1 <= X_endtime)
        before_230 = val1 <= X_endtime
        return before_230

    master_date_list = master_df["date"].tolist()

    is_before = pydash.map_(master_date_list, lambda x: filter_before230(x))
    master_df_before_230 = master_df[is_before]
    # print("master_df_before_230")
    # print(master_df_before_230)

    # Get the time before 2:30
    X_endtime = 14 * 60 + 30

    def to_day(tmp_date):
        new_date_string = "%4d-%02d-%02d" % (tmp_date.year, tmp_date.month, tmp_date.day)
        return new_date_string

    master_df_before_230_date_strings = pydash.map_(master_df_before_230['date'].tolist(), to_day)

    master_df_before_230.loc[:, 'new_date'] = pd.Series(master_df_before_230_date_strings,
                                                        index=master_df_before_230.index)

    master_df_before_230 = master_df_before_230.drop(['date', 'code'], axis=1)

    date_record_count_dict = pydash.chain(master_df_before_230["new_date"].tolist()).count_by().value()

    extracting_date_list = []
    for key in date_record_count_dict.keys():
        value = date_record_count_dict[key]
        if value >= 42:
            extracting_date_list.append(key)
        pass

    if len(extracting_date_list) == 0:
        return None

    extraction_settings = ComprehensiveFCParameters()
    extract_result = extract_features(master_df_before_230,
                                      column_id="new_date",
                                      impute_function=impute,
                                      default_fc_parameters=extraction_settings)
    if df_day is None:
        return extract_result
    ###### deal after

    trade_day_list = df_day["date"].tolist()
    trade_day_open = df_day["open"].tolist()
    next_day_open_dict = dict(zip(trade_day_list[:-1], trade_day_open[1:]))
    # print("next_day_open_dict", next_day_open_dict)

    def filter_after230_and_to_cal(tmp_date):
        new_date_string = "%4d-%02d-%02d" % (tmp_date.year, tmp_date.month, tmp_date.day)
        if not pydash.includes(extracting_date_list, new_date_string):
            return False
        val1 = (tmp_date.hour * 60 + tmp_date.minute)
        # print("date", date, val1, X_endtime, val1 <= X_endtime)
        before_230 = val1 <= X_endtime
        return not before_230

    is_after = pydash.map_(master_date_list, lambda x: filter_after230_and_to_cal(x))
    master_df_after_230 = master_df[is_after]

    # print("master_df_after_230")
    # print(master_df_after_230)

    def map_func(kv):
        tmp_date = kv[0]
        row_list = kv[1]
        import pydash

        new_date_string = "%4d-%02d-%02d" % (tmp_date.year, tmp_date.month, tmp_date.day)
        if not pydash.includes(extracting_date_list, new_date_string):
            return []
        next_day_open = pydash.get(next_day_open_dict, new_date_string, 0)

        if next_day_open > 0:
            max_value = pydash.chain(row_list).map(lambda row: row.close).max().value()
            # print("row_list", list(row_list))
            # print("max_value", max_value)
            label = (next_day_open - max_value) / max_value
            # tmp_dict = {
            #     "date": new_date_string,
            #     "label":label
            # }
            # print("new_date_string",new_date_string)
            # print()
            return [[new_date_string, label]]
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


    extract_result["label"] = result
    extract_result = extract_result.dropna()

    if csv_path_features is not None:
        extract_result.to_csv(csv_path_features, index=True)

    return extract_result


def save_daily_features_data(extract_result):
    new_date_list = pydash.uniq(extract_result["id"].tolist())
    new_date_list = pydash.uniq(extract_result["code"].tolist())
    for new_date in new_date_list:
        partial_data = extract_result[extract_result["id"] == new_date]
    pass