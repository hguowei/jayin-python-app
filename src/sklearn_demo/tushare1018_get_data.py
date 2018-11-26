
import pandas as pd

import tushare

code = "000001"
start = "2018-01-01"
end = "2018-10-18"
ktype="5"
csv_path = "data/data.%s.%s.%s.%s.csv" % (code, ktype, start, end)
import os
if os.path.exists(csv_path):
    print("Path exists!")
    data = pd.read_csv(csv_path)
else:
    data = tushare.get_k_data(code=code,
                              start=start,
                              end=end,
                              ktype=ktype)

print("data", type(data))
print(data)

data.to_csv(csv_path, index=False)
print("Saving to %s!" % csv_path)

# data <class 'pandas.core.frame.DataFrame'>
#                  date   open  close   high    low    volume    code
# 0    2018-09-27 14:55  10.72  10.72  10.73  10.70   20339.0  000001
# 1    2018-09-27 15:00  10.72  10.74  10.74  10.70   20502.0  000001
# 2    2018-09-28 09:35  10.78  10.91  10.92  10.78   88075.0  000001
# 3    2018-09-28 09:40  10.91  10.92  10.92  10.87   70369.0  000001
# 4    2018-09-28 09:45  10.93  10.89  10.94  10.88   62905.0  000001
# 5    2018-09-28 09:50  10.89  10.88  10.92  10.87   39683.0  000001