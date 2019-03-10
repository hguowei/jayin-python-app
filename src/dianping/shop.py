import random
import time
import datetime

import requests

import pandas as pd
import os

from utils import download

data = pd.read_csv("shop_list.csv")
print("data", data)

for shop_id, shop_url in zip(data["shop_id"].tolist(), data["shop_url"].tolist()):
    print("shop_id=", shop_id, ", shop_url=", shop_url)
    html_path = 'htmls/%s.html' % shop_id
    if os.path.exists(html_path):
        print("continue!")
        continue
    html = download(shop_url)

    with open(html_path, 'wb') as f:
        f.write(html)
