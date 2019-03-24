# -*- coding: utf-8 -*-
"""
Created on Fri May 11 09:02:12 2018
@author: JJ
"""
import urllib.request
import re
import pydash


def get_proxy(n):
    url = 'http://www.xicidaili.com/nn/{}'.format(n)
    headers = ('User-Agent',
               'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)
    html = opener.open(url).read().decode('utf8')
    ip_port_list = re.findall(r'<tr class(.*?)</tr>', html, re.S)
    proxy_list = []
    for i in ip_port_list:
        ip = re.findall(r'\d+\.\d+\.\d+\.\d+', i)[0]
        port = re.findall(r'<td>(\d+)</td>', i)[0]
        proxy = '{}:{}'.format(ip, port)
        proxy_list.append(proxy)
        print(proxy_list)
    return proxy_list


if __name__ == '__main__':
    proxy_list = get_proxy(1)
    new_list = pydash.uniq(proxy_list)
    tmp_dict = {
        "proxy_list": proxy_list
    }
    import json

    with open("proxy_list.json", "w") as f:
        json.dump(tmp_dict, f)
    with open("proxy_list.json", "r") as f:
        result = json.load(f)
    print("result", result["proxy_list"])
