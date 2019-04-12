import random
import time
import datetime

import requests


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


COOKIES = 'hc.v=3cd5047e-2489-a594-e948-6bb5f46ac847.1548813252;_lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic;_lxsdk=1689c76b3a5c8-0f8e9405104432-10336653-13c680-1689c76b3a5c8;_lxsdk_cuid=1689c76b3a5c8-0f8e9405104432-10336653-13c680-1689c76b3a5c8;_lxsdk_s=168a317b050-6f0-5d4-cda%7C%7C30;cy=1;cye=shanghai;s_ViewType=10;'

_cookies = _format_cookies(COOKIES)
_css_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}
_default_headers = {
    'Connection': 'keep-alive',
    'Host': 'www.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}


def download_shop(shop_id=3561973):
    _cur_request_url = 'http://www.dianping.com/shop/{}/'.format(shop_id)

    _delay_func()
    print('[{now_time}] {msg}'.format(now_time=datetime.datetime.now(), msg=_cur_request_url))

    res = requests.get(_cur_request_url, headers=_default_headers, cookies=_cookies)

    html = res.content
    # html = html.decode("utf-8", "ignore")

    with open('htmls/%s.html' % shop_id, 'wb') as f:
        f.write(html)

    return True
