import requests
import random
from bs4 import BeautifulSoup as bs


def _get_free_proxies():
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


def get_session():
    proxies = _get_free_proxies()
    for i in range(len(proxies)):
        # construct an HTTP session
        session = requests.Session()
        # choose one random proxy
        proxy = random.choice(proxies)
        session.proxies = {"http": proxy, "https": proxy}
        try:
            check_valid = session.get("http://icanhazip.com", timeout=1.5)
            if check_valid.status_code == 200:
                if len(check_valid.text.strip()) > 100:
                    continue
                print("Request page with IP:", check_valid.text.strip())
                return session
        except Exception as e:
            continue


if __name__ == '__main__':
    get_session()
