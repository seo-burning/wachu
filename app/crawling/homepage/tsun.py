#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
from random import choice
from bs4 import BeautifulSoup
import csv
import re
from decimal import Decimal

_user_agents = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
]

shopee_color_list_duplicate = []
shopee_size_list_duplicate = []


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


# In[2]:


def get_cleaned_price(price):
    return int(price/100)


def calculate_discount_rate(original_price, discount_price):
    discount_rate = int((1 - Decimal(discount_price)/Decimal(original_price))*100)
    return discount_rate


def get_cleaned_text(text):
    text = text.replace(' ', '').replace('\x08', '').strip().lower()
    return text


def get_product_image_dict(source):
    product_image = {
        'source': source,
        'source_thumb': source,
        'post_image_type': 'P'
    }
    return product_image


def get_option_from_script(script_list):
    option_json = None
    for script in script_list:
        try:
            script = script.string
            option_string = re.search(r'(?<="product-select",).*', script)
            option_string = option_string.group().replace('});', '').replace(
                ', onVariantSelected: selectCallback', '').replace('{ product: ', '').strip()
            option_json = option_string
            print(option_json)
        except:
            pass
    return option_json


def define_type(option_a, option_b):
    option_a = get_cleaned_text(option_a)
    option_b = get_cleaned_text(option_b)
    size_option_list = ['defaulttitle', 'xs', 's', 'm', 'l', 'xl', 'free', 'freesize', '25', '26', '27', '28',
                        '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '1', '2', '3', '4', '5']
    if option_a in size_option_list:
        size_obj = {'display_name': get_cleaned_text(option_a)}
        color_obj = {'display_name': get_cleaned_text(option_b)}
    else:
        size_obj = {'display_name': get_cleaned_text(option_b)}
        color_obj = {'display_name': get_cleaned_text(option_a)}
    return size_obj, color_obj


def define_type_single(option):
    option = get_cleaned_text(option)
    size_option_list = ['defaulttitle', 'xs', 's', 'm', 'l', 'xl', 'free', 'freesize', '25', '26', '27', '28',
                        '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '1', '2', '3', '4', '5']
    if option in size_option_list:
        size_obj = {'display_name': get_cleaned_text(option)}
        color_obj = None
    else:
        size_obj = None
        color_obj = {'display_name': get_cleaned_text(option)}
    return size_obj, color_obj


# In[6]:


def sub_crawler(obj, product_source, url_obj, duplicate_check_list):
    obj = HomepageCrawler()
    product_list = []
    store = 299
    for product_obj in product_source:
        is_discount = False
        #     link and get json
        product_link_soup = product_obj.find("a", href=True)
        product_link = "https://tsunsg.com"+product_link_soup.get('href')
        print(product_link)
        if product_link not in duplicate_check_list:
            try:
                response = obj.request_url(product_link)
                product_soup = BeautifulSoup(response.text, 'html.parser')
                script_list = product_soup.find_all('script')
                option_json = get_option_from_script(script_list)
                option_json = json.loads(option_json)
            except:
                continue

            #     title / description
            created_at = option_json['published_at'].replace('Z', '')
            name = option_json['title']
            description = option_json['description']

            original_price = get_cleaned_price(option_json['price'])
            discount_price = None
            discount_rate = None
            is_discount = False
            if (option_json['compare_at_price_max'] != 0.0) & (option_json['price'] != option_json['compare_at_price_max']):
                is_discount = True
                discount_price = get_cleaned_price(option_json['price'])
                original_price = get_cleaned_price(option_json['compare_at_price_max'])
                discount_rate = calculate_discount_rate(original_price, discount_price)
            else:
                discount_price = None
                discount_rate = None
                is_discount = False

            #      images
            product_image_list = []
            product_images = option_json['images']
            for product_image in product_images:
                source = product_image
                product_image = get_product_image_dict(source)
                product_image_list.append(product_image)
            product_thumbnail_image = option_json['featured_image'].replace(
                '.jpg', '_large.jpg').replace('.jpeg', '_large.jpeg')

        #     product options
            product_option_list = []
            shopee_size_list = []
            shopee_color_list = []
            stock = 99999
            if option_json:
                stock = 0
                for product_option in option_json['variants']:
                    option1 = product_option['option1']
                    option2 = product_option['option2']
                    option3 = product_option['option3']
                    if option3:
                        size_obj, color_obj = define_type(option1, option3)
                    elif option2:
                        size_obj, color_obj = define_type(option1, option2)
                    else:
                        size_obj, color_obj = define_type_single(option1)
                    if color_obj and color_obj not in shopee_color_list:
                        shopee_color_list.append(color_obj)
                    if size_obj and size_obj not in shopee_size_list:
                        shopee_size_list.append(size_obj)
                    option_stock = product_option['inventory_quantity']
                    if int(option_stock) < 0:
                        option_stock = 0
                    stock = stock + option_stock
                    product_option_obj = {
                        'is_active': product_option['available'],
                        'name': product_option['title'],
                        'original_price': original_price,
                        'discount_price': discount_price,
                        'currency': 'VND',
                        'size': size_obj,
                        'color': color_obj,
                        'stock': option_stock, }
                    product_option_list.append(product_option_obj)

        #     product size
            print(shopee_size_list)
            product_obj = {'is_active': False,
                           'is_discount': is_discount,
                           'created_at': created_at,
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
                           'discount_price': discount_price,
                           'discount_rate': discount_rate,
                           'currency': 'VND',
                           'is_free_ship': False,
                           'stock': stock,
                           'shopee_size': shopee_size_list,
                           'shopee_color': shopee_color_list,
                           'shopee_category': [],
                           'size_chart': None,
                           'productOption': product_option_list,
                           'style': 'street'

                           }
            product_list.append(product_obj)
        else:
            print('duplicated')
    return product_list, duplicate_check_list


def get_tsun():
    print('operating tsun crawler')
    obj = HomepageCrawler()
    url_list = ['all', ]
    product_list = []
    duplicate_check_list = []
    for url_obj in url_list:
        i = 1
        while True:
            url = "https://tsunsg.com/collections/"+url_obj+"?page=" + str(i)
            response = obj.request_url(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            product_source = soup.find_all("div", class_="product-block")
            product_sub_list, duplicate_check_list = sub_crawler(obj, product_source,
                                                                 url_obj,
                                                                 duplicate_check_list)
            product_list = product_list + product_sub_list
            length = len(product_source)
            print(length)
            if length == 0:
                break
            i = i+1
    return product_list
