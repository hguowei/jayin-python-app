import urllib.request
import re
import time
import random

from src.demo.proxy_list_get import get_proxy


def get_proxy_test2(n):
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
        return proxy_list


def proxy_read(proxy_list, i):
    proxy = proxy_list[i]
    print('当前IP为:{}'.format(proxy))
    sleep_time = random.randint(1, 3)
    print('等待{}秒'.format(sleep_time))
    time.sleep(sleep_time)
    print('开始测试')

    proxy_jj = urllib.request.ProxyHandler({'http': proxy})
    opener = urllib.request.build_opener(proxy_jj, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)

    try:
        html = urllib.request.urlopen('http://httpbin.org/ip')
        rhtml = html.read()
        print(rhtml)

    except Exception as e:
        print(e)
        print('-------IP不能用------')


if __name__ == '__main__':
    proxy_list = get_proxy(1)
    print('开始测试', len(proxy_list))

    for i in range(100):
        proxy_read(proxy_list, i)
