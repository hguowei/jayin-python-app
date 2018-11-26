#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd

code = "000001"
start = "2018-01-01"
end = "2018-10-18"
csv_path = "data/data.%s.D.csv" % code
# data = pd.read_csv(csv_path, index_col='date', parse_dates=True)
data = pd.read_csv(csv_path)

print(data.head())
#               open   close    high     low     volume  code
# date
# 2018-01-02  13.138  13.482  13.709  13.108  2081592.0     1
# 2018-01-03  13.512  13.118  13.640  12.990  2962498.0     1
# 2018-01-04  13.108  13.039  13.157  12.921  1854509.0     1
# 2018-01-05  13.000  13.089  13.138  12.941  1210312.0     1
# 2018-01-08  13.039  12.754  13.079  12.656  2158620.0     1
# 2018-01-09  12.754  12.872  12.990  12.715  1344345.0     1


# In[22]:



date = data.index[0]
print('date', type(date), date)

#last_day_index = data.index + pd.offsets.Day(-1)
last_day_index = data.index + 1
print("last_day_index", type(last_day_index), last_day_index)

series = data["close"]

last_day_close = pd.Series(series.values, index=last_day_index)

data["last_day_close"] = last_day_close

data["today_increase"] = (data["close"] - data["last_day_close"]) / data["last_day_close"]

pass


# In[23]:


series.head()


# In[24]:


last_day_close.head()


# In[25]:


(13.118 - 13.482) / 13.482


# In[26]:


idx = 1
(data["close"][idx] - data["last_day_close"][idx]) / data["last_day_close"][idx]


# In[27]:


(data["close"][idx] - data["last_day_close"][idx])


# In[28]:


data.head()


# In[ ]:




