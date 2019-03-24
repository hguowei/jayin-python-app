import requests, re, os
from pprint import pprint

down_dir = os.path.join(os.getcwd(), 'daili_IP/')

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/63.0.3239.84 Safari/537.36',
           'Referer': 'https://www.xicidaili.com/nt/',
           'Connection': 'keep-alive',
           'Host': 'www.xicidaili.com'}

url = 'https://www.xicidaili.com/nn/'


def main():
    print('--开始爬取代理IP--')
    req = requests.get(url, headers=headers, verify=False)
    # print(req.text)
    ip = re.findall('<td>(\d*\.\d*\.\d*\.\d*)</td>', req.text)
    port = re.findall('<td>(\d*)</td>', req.text)
    dic = dict(zip(ip, port))
    pprint(dic)
    with open(down_dir + 'ip.txt', 'w') as f:
        for i in range(len(ip)):
            f.write(ip[i] + ':' + str(port[i] + '\n'))
    print('IP地址保存在:' + down_dir)


if __name__ == '__main__':
    if not os.path.exists(down_dir):
        os.mkdir(down_dir)
    main()
