#!/usr/bin/env python
# coding: utf-8

# In[13]:

import time
import pandas as pd
from pyspark.sql import SparkSession
from tsfresh import extract_features
from tsfresh.feature_extraction import ComprehensiveFCParameters
from tsfresh.utilities.dataframe_functions import impute
import pydash

start_time = time.time()

spark = SparkSession.builder \
    .master("local") \
    .appName("Word Count") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

code = "000001"
start = "2018-01-02"
end = "2018-01-02"
ktype = "5"
csv_path = "data/data.000001.5.2018-01-02.2018-01-02.csv"
csv_path = "data/data.%s.%s.%s.%s.csv" % (code, ktype, start, end)
day_csv_path = "data/data.%s.D.csv" % code

# master_df = pd.read_csv(csv_path, index_col='date', parse_dates=True)
master_df = pd.read_csv(csv_path)

df_day = pd.read_csv(day_csv_path)
day_open_dict = dict(pydash.chain(df_day["date"].tolist()).zip(df_day["open"].tolist()).value())

# print(day_open_dict.keys())
# print(type(list(day_open_dict.keys())[0]))
# exit()
# print("day_open_dict", day_open_dict)
# print("day_open_dict", day_open_dict[df_day["date"][0]])
# print(df_day.head())
# exit()

print(master_df.head())

first_date = pd.Timestamp(master_df["date"][0]) + pd.offsets.Hour(7)


def to_new_date(date):
    if not isinstance(date, pd.Timestamp):
        date = pd.Timestamp(date)

    return int("%04d%02d%02d" % (date.year, date.month, date.day))


master_df["date"] = master_df["date"].apply(pd.Timestamp)
master_df = master_df[master_df["date"].apply(pd.Timestamp) > first_date]
print(master_df.head())

# Get the time before 2:30
X_endtime = 14 * 60 + 30


def filter_before230(row, is_filter_before=True):
    date = row.date
    # val1 = (date.hour * 60 + date.minute)
    # print("date", date, val1, X_endtime, val1 <= X_endtime)
    before_230 = (date.hour * 60 + date.minute) <= X_endtime
    if is_filter_before:
        return before_230
    else:
        return not before_230

    # return date.hour == 14


master_df_before_230 = master_df[master_df.apply(lambda row: filter_before230(row, True), axis=1)]
master_df_after_230 = master_df[master_df.apply(lambda row: filter_before230(row, False), axis=1)]

print("master_df_before_230", master_df_before_230.head())

# master_df_after_230
#                   date   open  close   high    low   volume  code
# 44  2018-09-28 14:35:00  10.97  11.00  11.00  10.96  17900.0     1
# 45  2018-09-28 14:40:00  11.00  11.00  11.01  10.97  38767.0     1
# 46  2018-09-28 14:45:00  11.00  11.00  11.01  10.98  28361.0     1
# 47  2018-09-28 14:50:00  11.00  11.02  11.04  11.00  28804.0     1
# 48  2018-09-28 14:55:00  11.02  11.06  11.06  11.02  45205.0     1
# 49  2018-09-28 15:00:00  11.06  11.05  11.06  11.05  27174.0     1
# 92  2018-10-08 14:35:00  10.57  10.56  10.59  10.55  20832.0     1
# 93  2018-10-08 14:40:00  10.55  10.57  10.58  10.55  18302.0     1
# 94  2018-10-08 14:45:00  10.57  10.53  10.58  10.52  50443.0     1
# 95  2018-10-08 14:50:00  10.54  10.50  10.55  10.50  63060.0     1
# 96  2018-10-08 14:55:00  10.50  10.49  10.51  10.46  52757.0     1
# 97  2018-10-08 15:00:00  10.49  10.45  10.51  10.45  28848.0     1
print("master_df_after_230", master_df_after_230.head())

print("cccc", master_df_before_230.columns)


def to_day(tmp_date):
    new_date_string = "%4d-%02d-%02d" % (tmp_date.year, tmp_date.month, tmp_date.day)
    return new_date_string


xxx = pydash.map_(master_df_before_230['date'].tolist(), to_day)

master_df_before_230['new_date'] = pd.Series(xxx, index=master_df_before_230.index)

master_df_before_230 = master_df_before_230.drop(['date', 'code'], axis=1)

print("master_df_before_230", master_df_before_230)


def map_func(kv):
    tmp_date = kv[0]
    row_list = kv[1]
    import pydash

    new_date_string = "%4d-%02d-%02d" % (tmp_date.year, tmp_date.month, tmp_date.day)
    next_day_open = pydash.get(day_open_dict, new_date_string, 0)
    print("XXXX open", next_day_open)

    if next_day_open > 0:
        max_value = pydash.chain(row_list).map(lambda row: row.close).max().value()
        print("max_value", max_value)
        return [[new_date_string, (max_value - next_day_open) / next_day_open]]
    else:
        return []


def to_kv_func(row):
    from datetime import datetime
    tmp_date = row.date
    new_date = datetime(tmp_date.year, tmp_date.month, tmp_date.day)
    return new_date, row


#
max_can_buy = spark.createDataFrame(master_df_after_230).rdd.map(to_kv_func).groupByKey().flatMap(map_func).collect()
print("max_can_buy", max_can_buy)

date_list = pydash.map_(max_can_buy, lambda kv: kv[0])
value_list = pydash.map_(max_can_buy, lambda kv: kv[1])

result = pd.Series(value_list, index=date_list)
test = pd.read_csv("test.index.csv", index_col='id')

test["value"] = result


test = test.dropna()

test.to_csv("test2.csv", index=False)
exit()

extraction_settings = ComprehensiveFCParameters()
X = extract_features(master_df_before_230,
                     column_id="new_date",
                     impute_function=impute,
                     default_fc_parameters=extraction_settings)

print("X", type(X), X.shape)
print("X", X.index)
print("X", X.columns)

X.to_csv("test.index.csv")
X.to_csv("test.csv", index=False)
print("Program cost %3fs." % (time.time() - start_time))
