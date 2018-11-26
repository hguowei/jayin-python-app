import os
try:
    CURRENT_DIR = os.path.dirname(__file__)
except Exception as e:
    CURRENT_DIR = os.getcwd()
PROJECT_PATH = os.path.dirname(os.path.dirname(CURRENT_DIR))

print("PROJECT_PATH", PROJECT_PATH)
import pydash
import pandas as pd

path = PROJECT_PATH + "/data/AirPassengers.csv"


data = pd.read_csv(path)

print(data.head())

date_parser = lambda dates: pd.datetime.strptime(dates, "%Y-%m")
data = pd.read_csv(path, parse_dates=["Month"], index_col="Month", date_parser=date_parser)
print(data.head())