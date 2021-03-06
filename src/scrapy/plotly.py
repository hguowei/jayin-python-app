# Learn about API authentication here: https://plot.ly/pandas/getting-started
# Find your api_key here: https://plot.ly/settings/api

import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

#df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
df = pd.read_csv("/Users/huang/Downloads/finance-charts-apple.csv")

data = [go.Scatter( x=df['Date'], y=df['AAPL.Close'] )]

py.iplot(data, filename='pandas-time-series')