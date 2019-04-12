import codecs
import datetime
import os
import random
import time

import pydash
import requests
from lxml import etree


def _format_cookies(cookies):
    cooks = {}
    for cookie in cookies.replace(' ', '').split(';'):
        # print("cookie", cookie)
        if len(cookie) > 0:
            splits = cookie.split('=')
            cooks[splits[0]] = splits[1]
    # cookies = {cookie.split('=')[0]: cookie.split('=')[1]
    #            for cookie in cookies.replace(' ', '').split(';')}

    return cooks


def _delay_func(_delay=10):
    delay_time = random.randint((_delay - 2) * 10, (_delay + 2) * 10) * 0.1
    time.sleep(delay_time)


COOKIES = "_hc.v=3cd5047e-2489-a594-e948-6bb5f46ac847.1548813252;_lxsdk=1689c76b3a5c8-0f8e9405104432-10336653-13c680-1689c76b3a5c8_lxsdk_cuid=1689c76b3a5c8-0f8e9405104432-10336653-13c680-1689c76b3a5c8;_lxsdk_s=16962b3c607-bf8-14-319%7C%7C177;cy=1;cye=shanghai;navCtgScroll=0;s_ViewType=10;showNav=#nav-tab|0|0;"
_cookies = _format_cookies(COOKIES)
# _css_headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
# }
_default_headers = {
    'Connection': 'keep-alive',
    'Host': 'www.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}


def download(url):
    _delay_func()
    print('[{now_time}] {msg}'.format(now_time=datetime.datetime.now(), msg=url))

    res = requests.get(url, headers=_default_headers, cookies=_cookies)

    html = res.content
    # html = html.decode("utf-8", "ignore")
    return html


def read_html(path):
    f = codecs.open(path, "r", "utf-8")
    s = f.readline()
    print("S", s)
    f.close()
    return pydash.join(s, "")


def read_file(path):
    f = open(path)
    s = f.read()
    f.close()
    return s


def to_string(element):
    return etree.tostring(element, encoding="utf-8", pretty_print=True)[:-1].decode("utf-8")


def list_files(file_dir, suffix):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == suffix:
                L.append(os.path.join(root, file))
    return L


def find_file(file_dir, suffix):
    results = []
    for root, dirs, files in os.walk(file_dir):
        # for filename in files:
        #     print("file:%s" % filename)
        # for dirname in dirs:
        #     print("dir:%s" % dirname)
        for filename in files:
            print("filename", filename, suffix, pydash.ends_with(filename, suffix))
            if pydash.ends_with(filename, suffix):
                results.append("%s/%s" % (root, filename))
    return results


def to_shorter_file_name(css_file, surfix):
    idx = pydash.last_index_of(css_file, "/")
    if idx >= 0:
        file_name = css_file[idx + 1:]
    else:
        file_name = css_file

    print("file_name", file_name)
    new_file_name = pydash.replace(file_name, "_mod_easy-login", "")
    print("new_file_name", new_file_name)
    new_css_file = pydash.replace(css_file, file_name, new_file_name)
    return "%s.%s" % (new_css_file, surfix)

#
# result = find_file(".", "1eb515893adcc915f7b5cb7d12b8772f.css")
# print("result", result)
#
# print(pydash.ends_with("1eb515893adcc915f7b5cb7d12b8772f.css", "1eb515893adcc915f7b5cb7d12b8772f.css"))
