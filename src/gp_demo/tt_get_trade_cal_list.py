from datetime import datetime
from tools.daily_data import get_daily_data
from tools.get_all_data import get_trade_cal_list2, get_trade_cal_list
from utils import get_codes

now_date = datetime.now()


codes = get_codes()

code = codes[0]
daily_data = get_daily_data(code, just_download=False)

dates = daily_data["date"].tolist()

code = codes[1]
daily_data = get_daily_data(code, just_download=False)

date2 = daily_data["date"].tolist()

print("dates", dates)
dates.extend(date2)

print("date2", date2)

import pydash
print(pydash.uniq(dates))


print("aaaaa", get_trade_cal_list())
print("aaaaa", get_trade_cal_list2(now_date))