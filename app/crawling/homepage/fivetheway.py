#!/usr/bin/env python
# coding: utf-8

# In[150]:


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

url = "https://docs.google.com/forms/d/e/1FAIpQLSfMPLIj19QrPny-_GVgVBeRVLIxDCVDV2KSvx7koqZmbFXCEw/viewform"
store = 292


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


# In[151]:


# In[152]:


def find_thumbnail(name, product_thumbnail_container):
    index = name[1:].find('/')
    name = name[0:index+2]
    for product_thumb_img in product_thumbnail_container:
        if product_thumb_img['name'] == name:
            return product_thumb_img['product_thumbnail_image']


# In[153]:


def find_name(name):
    index = name[1:].find('/')
    name = name[0:index+2]
    return name


# In[154]:


def find_price(name):
    price_string = name.lower().replace('vnd', '').replace('vnđ', '').strip()[-8:]
    price = price_string.replace('.', '').strip()
    print(price)
    return price


# In[162]:
def get_product_image_dict(source):
    product_image = {
        'source': source,
        'source_thumb': source,
        'post_image_type': 'P'
    }
    return product_image


def get_5theway():
    obj = HomepageCrawler()
    i = 1
    url = "https://docs.google.com/forms/d/e/1FAIpQLSfMPLIj19QrPny-_GVgVBeRVLIxDCVDV2KSvx7koqZmbFXCEw/viewform"
    response = obj.request_url(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_list_soup = soup.find_all('div', class_='freebirdFormviewerViewItemsItemItem')
    product_list = []
    product_thumbnail_container = []
    for product_obj in product_list_soup:
        print('------------------------------------------------------------')
        product_image_list = []
        name = product_obj.find('div', class_='freebirdFormviewerViewItemsItemItemTitleContainer')
        product_thumbnail_image = product_obj.find('img', class_='freebirdFormviewerViewItemsEmbeddedobjectImage')
        product_obj.find_all('div', class_='freebirdFormviewerViewItemsCheckboxContainer')
        product_size_list = product_obj.find_all('span', class_='docssharedWizToggleLabeledLabelText')
        if product_thumbnail_image:
            product_thumbnail_image = product_thumbnail_image.get('src')
        if name:
            name = name.text
            print(name)
            if name[0] == '/' and len(product_size_list) == 0:
                print('this is product thumb image containing object')

                name = find_name(name)
                product_thumbnail_container.append({'name': name, 'product_thumbnail_image': product_thumbnail_image})
                continue
            elif name[0] == '/' and name[-1] == 'Đ':
                if product_thumbnail_image:
                    print('i have image with me')
                    product_image = get_product_image_dict(product_thumbnail_image)
                    product_image_list.append(product_image)
                else:
                    print('this is actual product')
                    product_thumbnail_image = find_thumbnail(name, product_thumbnail_container)
                    product_image = get_product_image_dict(product_thumbnail_image)
                    product_image_list.append(product_image)
            elif name[-1] == 'Đ':
                print('this is awkward product')
                product_thumbnail_image = "https://i.pinimg.com/originals/9d/fd/a1/9dfda1dd1b65d576a275ee0f8742b7fa.jpg"
                product_image = get_product_image_dict(product_thumbnail_image)
                product_image_list.append(product_image)
            else:
                continue
            print('try to make product')
            original_price = find_price(name)

            product_obj.find_all('div', class_='freebirdFormviewerViewItemsCheckboxContainer')
            product_size_list = product_obj.find_all('span', class_='docssharedWizToggleLabeledLabelText')
            product_option_list = []
            shopee_size_list = []
            if product_size_list:
                for product_size in product_size_list:
                    print(product_size.text)
                    display_name = product_size.text
                    shopee_size_list.append({'display_name': display_name})
                    stock = 99999
                    total_stock = 99999
                    option_name = product_size.text
                    product_option_obj = {
                        'is_active': True,
                        'name': option_name,
                        'original_price': original_price,
                        'discount_price': None,
                        'currency': 'VND',
                        'stock': stock, }
                    product_option_list.append(product_option_obj)
            product = {'is_active': False,
                       'is_discount': False,
                       'current_review_rating': 0,
                       'product_source': 'HOMEPAGE',
                       'product_link': url,
                       'store': store,
                       'name': name,
                       'description': name,
                       'product_image_type': 'SP',
                       'product_thumbnail_image': product_thumbnail_image,
                       'product_image_list': product_image_list,
                       'video_source': None,
                       'original_price': original_price,
                       'discount_price': 0,
                       'discount_rate': 0,
                       'currency': 'VND',
                       'is_free_ship': False,
                       'stock': total_stock,
                       'shopee_color': [],
                       'shopee_size': shopee_size_list,
                       'shopee_category': [],
                       'size_chart': None,
                       'productOption': product_option_list
                       }
            print('i gonna add')
            product_list.append(product)
    return product_list
