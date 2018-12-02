import pydash
from pyspark.sql import SparkSession

from feature_tools import do_extract_feature
from tools.daily_data import get_daily_data
from tools.five_minite_data import get_min_data

spark = SparkSession.builder \
    .master("local") \
    .appName("Word Count") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

code = "000957"
quering_date = "2018-11-29"
csv_path_features = None

daily_data = get_daily_data(code, just_download=False)
print("daily_data")
print(daily_data)

minites_data = get_min_data(code, quering_date=quering_date, is_for_train_not_eval=True,
                            just_download=False)
print("minites_data")
print(minites_data)

master_df = minites_data

df_features = do_extract_feature(spark, master_df, daily_data, csv_path_features)

old_columns = master_df.columns.tolist()
print("df_features", df_features)

for feature in df_features.columns.tolist():
    is_old = False
    for old_feature in old_columns:
        if pydash.starts_with(feature, old_feature):
            is_old = True
    if not is_old:
        print("new", feature)
