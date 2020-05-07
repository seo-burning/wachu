#!/usr/bin/env python
# coding: utf-8

# In[41]:


import requests
import json
from random import choice
from bs4 import BeautifulSoup
import csv


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


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxy_list = soup.find('tbody')
    proxies = set()
    for rows in proxy_list.find_all('tr')[:5]:
        proxies.add(rows.find_all('td')[0].text +
                    ':'+rows.find_all('td')[1].text)
    return proxies


class HomepageCrawler:
    def __init__(self, user_agents=None, proxy=None):
        self.user_agents = user_agents
        self.proxy = proxy

    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(_user_agents)

    def __random_proxies(self):
        if self.proxy and isinstance(self.proxy, list):
            # print('execute')
            return choice(self.proxy)
        proxies = get_proxies()
        return random.sample(get_proxies(), 1)[0]

    def request_url(self, url):
        try:
            response = requests.get(url,
                                    headers={'User-Agent': self.__random_agent(),
                                             'X-Requested-With': 'XMLHttpRequest',
                                             },
                                    proxies={'http': self.proxy, 'https': self.proxy})
            response.raise_for_status()
        except requests.HTTPError as e:
            # print(e)
            pass
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response

#     @staticmethod


def extract_json_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('body')
    script_tag = body.find('script')
    raw_string = script_tag.text.strip().replace(
        'window._sharedData =', '').replace(';', '')
    return json.loads(raw_string)


# In[45]:


def get_cleaned_price(price):
    cleaned_price = price.lower().replace(',', '').replace('₫', '').strip()
    return cleaned_price


def get_product_image_dict(source):
    product_image = {
        'source': source,
        'source_thumb': source,
        'post_image_type': 'P'
    }
    return product_image


# In[67]:


def get_swe():
    obj = HomepageCrawler()
    product_list = []
    url_list = ['new-arrivals', 'tops', 'outerwear', 'bottoms', 'accessories']
    for url_obj in url_list:
        url = "https://swe.vn/collections/" + url_obj
        response = obj.request_url(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        products_soup = soup.find('body').find_all('div', class_='single-product')
        product_sub_list = get_product_sub_list(products_soup)
        product_list = product_list + product_sub_list
    return product_list


# In[72]:


def get_product_sub_list(products_soup):
    store = 296
    product_list = []
    for ps in products_soup:
        product_link = 'http://swe.vn' + ps.find('div', class_='product-img').find('a').get('href')
        name = ps.find('h2')
        if name:
            name = name.text
            description = name
        else:
            continue

        price = ps.find('div', class_='price-box')
        if price:
            price = price.find('span').text
            original_price = get_cleaned_price(price)
        product_thumbnail_image = "http:" + \
            ps.find('div', class_='product-img').find('img', class_='visible-xs').get('src')

        product_image_list = []
        product_images = ps.find('div', class_='product-img').find_all('img', class_='hidden-xs')
        for product_image in product_images:
            source = "http:" + product_image.get('src')
            product_image = get_product_image_dict(source)
            product_image_list.append(product_image)

        print(name, price, product_thumbnail_image, product_link, product_image_list)
        shopee_size_list = []
        product_option_list = []
        product_sizes = ps.find_all('span', class_='size-variant')
        total_stock = 0
        for product_size in product_sizes:
            display_name = product_size.text
            shopee_size_list.append({'display_name': display_name})
            if 'sold-out-variant' in product_size.get('class'):
                stock = 0
                is_active = False
                print('sold out')
            else:
                is_active = True
                stock = 99999
                total_stock = 99999
            option_name = product_size.text
            product_option_obj = {
                'is_active': is_active,
                'name': option_name,
                'original_price': original_price,
                'discount_price': None,
                'currency': 'VND',
                'stock': stock, }
            product_option_list.append(product_option_obj)

        product_obj = {'is_active': False,
                       'is_discount': False,
                       'current_review_rating': 0,
                       'product_source': 'HOMEPAGE',
                       'product_link': product_link,
                       'store': store,
                       'name': name,
                       'description': description,
                       'product_image_type': 'MP',
                       'product_thumbnail_image': product_thumbnail_image,
                       'product_image_list': product_image_list,
                       'video_source': None,
                       'original_price': original_price,
                       'discount_price': None,
                       'discount_rate': None,
                       'currency': 'VND',
                       'is_free_ship': False,
                       'stock': total_stock,
                       'shopee_size': shopee_size_list,
                       'shopee_color': [],
                       'shopee_category': [],
                       'size_chart': None,
                       'productOption': product_option_list
                       }
        product_list.append(product_obj)
    return product_list
