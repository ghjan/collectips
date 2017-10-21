# encoding = utf8
import urllib.request

import urllib.parse
import http.cookiejar
import re

from bs4 import BeautifulSoup
import urllib
import socket
import traceback

User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent

url_1 = r"http://ip.chinaz.com/getip.aspx"
url_2 = r'http://httpbin.org/ip'
url_3 = r'http://python.org/'

'''''
获取所有代理IP地址
'''


def getProxyIp():
    proxy = []
    for i in range(1, 2):
        try:
            url = 'http://www.xicidaili.com/nn/' + str(i)
            req = urllib.request.Request(url, headers=header)

            res = urllib.request.urlopen(req).read()
            soup = BeautifulSoup(res)
            ips = soup.findAll('tr')
            for x in range(1, len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                ip_temp = tds[1].contents[0] + "\t" + tds[2].contents[0]
                proxy.append(ip_temp)
        except Exception as e:
            print(e)
            continue
    return proxy


'''''
验证获得的代理IP地址是否可用
'''


def validateIp(proxy):
    f = open("ip.txt", "w")
    f.write("IPPOOL=[")
    socket.setdefaulttimeout(3)

    for i in range(0, len(proxy)):
        try:
            ip = proxy[i].strip().split("\t")
            proxy_ip_port = "http://" + ip[0] + ":" + ip[1]
            _get_data_withproxy(url_1, proxy_ip_port, data=None)
            f.write("{'ipaddr':'" + ip[0] + ":" + ip[1] + "'},\n")
        except Exception as e:
            continue
    f.write("]")
    f.close()


def _get_data_withproxy(url, proxy_ip_port=None, data=None):
    proxy = urllib.request.ProxyHandler({'http': proxy_ip_port})  # 设置proxy
    opener = urllib.request.build_opener(proxy)  # 挂载opener
    urllib.request.install_opener(opener)  # 安装opener
    if data:
        data = urllib.parse.urlencode(data).encode('utf-8')
        page = opener.open(url, data).read()
    else:
        page = opener.open(url).read()
    page = page.decode('utf-8')
    return page


def _get_data(url):
    response = urllib.request.urlopen(url)
    page = response.read()
    page = page.decode('utf-8')
    return page


if __name__ == '__main__':
    page = _get_data(url_1)
    proxy = getProxyIp()
    print("proxy:{}".format(proxy))
    if proxy:
        validateIp(proxy)
