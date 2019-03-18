# encoding: utf-8
import datetime
import random
import time
import re
import pydash

# from selenium.webdriver.chrome.options import Options
# from selenium import webdriver
from lxml import etree
import requests

from utils import read_file, to_string


def parse_comment_page(doc):
    """
        解析评论页并提取数据
    """
    datas = []
    for li in doc.xpath('//*[@class="mod comment"]/ul/li'):
        print("li", li)
        name = li.xpath('.//a[@class="name"]/text()')[0].strip('\n\r \t')
        try:
            star = li.xpath('.//span[contains(./@class, "sml-rank-stars")]/@class')[0]
            print("star1", star)
            star = re.search(r'sml-str(\d+)', star).group(1)
            print("star2", star)
        except IndexError:
            star = 0
        time = li.xpath('.//span[@class="time"]/text()')[0].strip('\n\r \t')
        # test = li.xpath('.//p[@class="desc J-desc"]/text()')
        # comment = pydash.join(test, "")
        # print("comment=")
        # print(comment)
        test = li.xpath('.//p[@class="desc J-desc"]')
        print("test", type(test), test)
        for comment_elem in test:
            # just one comment.
            print("comment_elem", type(comment_elem), comment_elem)
            comment = to_string(comment_elem)

            class_set = set()
            # <b class="([a-zA-Z0-9]{5,6})"/>
            for class_name in re.findall(r'<b class="([a-zA-Z0-9]{5,6})"/>', comment):
                origin_string = '<b class="%s"/>' % class_name
                print("class_name", class_name, origin_string)
                class_set.add(class_name)

            print("comment=")
            print(comment)

        score = ' '.join(map(lambda s: s.strip('\n\r \t'), li.xpath('.//span[@class="score"]//text()')))

        data = {
            'name': name,
            'comment': comment,
            'star': star,
            'score': score,
            'time': time,
        }
        datas.append(data)
        print("data", data)
        exit()

    return datas


file_path = "/Users/huang/Desktop/workpython/jayin-python-app/src/dianping/htmls/504634.html"
html = read_file(file_path)

doc = etree.HTML(html)
result = parse_comment_page(doc)
print("result", result)
