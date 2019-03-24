import os
import re

import pandas as pd
import pydash

from utils import read_file


# 目前餐馆列表是手动将页面ctrl+s保存的。


def get_files(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.htm':
                L.append(os.path.join(root, file))
    return L


files = get_files(file_dir="shop_lists")

shop_list_path = "shop_list.csv"
shop_df = None
shop_ids = []
if os.path.exists(shop_list_path):
    shop_df = pd.read_csv(shop_list_path)
    shop_ids = shop_df["shop_id"].tolist()

for file_path in files[:1]:
    # print("files=", files)
    # file_path = files[0]
    print("file_path", file_path)

    html = read_file(file_path)

    # pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式

    pattern = re.compile(
        r'http://www.dianping.com/shop/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式

    urls = re.findall(pattern, html)
    # print("urls", urls)


    def parse_url(url):
        idx = pydash.last_index_of(url, "/")
        shop_id = url[idx + 1:]
        try:
            shop_id = int(shop_id)
            if pydash.includes(shop_ids, shop_id):
                return []
            else:
                shop_ids.append(shop_id)
            print("shop_id", shop_id)

            return [{
                "shop_id": shop_id,
                "shop_url": "http://www.dianping.com/shop/%s" % shop_id,

            }]
        except:
            return []

    tmp_dict = pydash.chain(urls).map(parse_url).flatten().value()
    # print("tmp_dict", tmp_dict)

    data = pd.DataFrame(tmp_dict)
    # print("data", data)

    if data.empty:
        pass
    elif shop_df is None:
        shop_df = data
    else:
        shop_df = shop_df.append(data)

print("size", shop_df.size)
if shop_df is not None:
    shop_df.to_csv(shop_list_path, index=False)
