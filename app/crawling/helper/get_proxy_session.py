import re
import requests
import random
from bs4 import BeautifulSoup as bs
from random import choice

_user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 6.0; HTC One X10 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'
]

DEFAULT_PROXIES = ["1.251.31.43:80",
                   "1.255.48.197:8080",
                   "118.69.50.154:443",
                   "177.54.144.126:8",
                   "182.23.211.110:80",
                   "183.89.101.226:3128",
                   "196.27.119.131:80",
                   "81.201.60.130:80",
                   "88.199.21.76:80",
                   "95.216.10.19:3128",
                   "118.69.50.154:80",
                   "140.227.237.154:1000",
                   "201.48.165.189:8080",
                   "80.241.222.138:80",
                   "13.75.114.68:25222",
                   "139.59.129.114:3128",
                   "177.69.203.67:3128",
                   "20.43.156.109:80",
                   "80.241.222.137;80",
                   "91.205.174.26:80",
                   "162.14.18.11:80",
                   "20.44.193.208:80",
                   "20.43.156.27:80",
                   "46.4.129.55:80",
                   "213.136.78.253:5836",
                   "35.230.21.108:80", ]


def _get_free_proxies():
    print('P', end='')
    url = "https://free-proxy-list.net/"
    # get the HTTP response and construct soup object
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies


def _get_free_proxies_2():
    url = "https://www.proxynova.com/proxy-server-list"
    # get the HTTP response and construct soup object
    soup = bs(requests.get(url, headers={'User-Agent': choice(_user_agents),
                                         'X-Requested-With': 'XMLHttpRequest', }).content, "html.parser")
    proxies = []
    for row in soup.find_all("tr"):
        tds = row.find_all("td")
        try:
            ip = str(tds[0].find('script')).replace("<script>document.write('", '').replace("');</script>", '')
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            speed = tds[3].text.replace(' ms', '').strip()
            if (int(speed) > 1000):
                proxies.append(host)
        except IndexError:
            continue
    return proxies


def get_session(new=False, proxies=None):
    if new:
        try:
            proxies = _get_free_proxies() + DEFAULT_PROXIES
        except:
            proxies = DEFAULT_PROXIES
        try:
            proxies = proxies + _get_free_proxies_2()
        except:
            pass
    elif proxies and len(proxies) > 0:
        proxies = proxies
    else:
        try:
            proxies = _get_free_proxies()
        except:
            proxies = DEFAULT_PROXIES
        try:
            proxies = proxies + _get_free_proxies_2()
        except:
            pass
    for i in range(len(proxies)):
        # construct an HTTP session
        session = requests.Session()
        # choose one random proxy
        proxy = random.choice(proxies)
        session.proxies = {"http": proxy, "https": proxy}
        print('c', end='')
        try:
            check_valid = session.get("http://icanhazip.com", timeout=3)
            if check_valid.status_code == 200:
                if len(check_valid.text.strip()) > 100:
                    continue
                print("\nRequest page with IP:{}".format(check_valid.text.strip()))
                return session, proxies
        except Exception as e:
            proxies.pop(i)
            continue
    return session, proxies
