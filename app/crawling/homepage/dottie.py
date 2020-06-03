#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
from random import choice
from bs4 import BeautifulSoup
import csv


_user_agents = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
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


# In[2]:


def get_cleaned_price(price):
    cleaned_price = price.lower().replace(',', '').replace('₫', '').strip()
    return cleaned_price


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


def get_product_sub_list(products_soup, obj, url_obj, duplicate_check_list):
    store = 3
    product_list = []
    for ps in products_soup:
        try:
            product_link = 'https://dottie.vn' + ps.find('a', class_='product-link').get('href')
            if product_link not in duplicate_check_list:
                duplicate_check_list.append(product_link)
                print(product_link)
                name = ps.find('span', class_='product-name')
                name = name.text
                description = name
                is_active = True
                stock = 9999
                price = ps.find('span', class_='product-price')
                price = get_cleaned_price(price.find('span').text)
                is_discount = False
                discount_price = None
                discount_rate = None
                if (price == 'đã bán hết' or price == 'HÀNG SẮP VỀ' or price == '0₫' or price == 'hàng sắp về'):
                    continue
                original_price = get_cleaned_price(price)
                try:
                    int(original_price)
                except:
                    continue
                product_thumbnail_image = "http:"+ps.find('img', class_='product-image').get('src')

                response = obj.request_url(product_link)
                soup = BeautifulSoup(response.text, 'html.parser')

                product_image_list = []
                product_images = soup.find('div', class_='swiper-wrapper').find_all('img', class_='carousel-img')
                for product_image in product_images:
                    source = "http:" + product_image.get('src')
                    product_image = get_product_image_dict(source)
                    product_image_list.append(product_image)

                shopee_color_list = []
                shopee_size_list = []
                product_option_list = []
                option_list = soup.find_all('option')
                for option_obj in option_list:
                    option_obj = option_obj.text.strip()
                    print(option_obj)
                    try:
                        option_name = option_obj
                        index = option_obj.find('-')
                        color_obj, size_obj = option_obj[0:index].split('/')
                    except:
                        option_name = option_obj
                        index = option_obj.find('-')
                        option_obj = option_obj[:index] + option_obj[index+1:]
                        print(option_obj)
                        index = option_obj.find('-')
                        color_obj, size_obj = option_obj[0:index].split('/')
                    color_obj = {'display_name': get_cleaned_text(color_obj)}
                    size_obj = {'display_name': get_cleaned_text(size_obj)}
                    if color_obj not in shopee_color_list:
                        shopee_color_list.append(color_obj)
                    if size_obj not in shopee_size_list:
                        shopee_size_list.append(size_obj)
                    product_option_obj = {
                        'is_active': True,
                        'name': option_name,
                        'original_price': original_price,
                        'discount_price': discount_price,
                        'currency': 'VND',
                        'stock': stock,
                        'size': size_obj,
                        'color': color_obj}
                    product_option_list.append(product_option_obj)

                product_option_source_list = soup.find('div', class_='select').find('select').find_all('option')
                for product_option_source_obj in product_option_source_list:
                    option_disabled = product_option_source_obj.get('disabled')
                    if option_disabled:
                        color_obj, size_obj = product_option_source_obj.text.strip().replace(' - Đã bán hết', '').split('/')
                        color_obj = {'display_name': get_cleaned_text(color_obj)}
                        size_obj = {'display_name': get_cleaned_text(size_obj)}
                        for product_option_obj in product_option_list:
                            if (product_option_obj['color'] == color_obj and product_option_obj['size'] == size_obj):
                                product_option_obj.update({'stock': 0})
                                product_option_obj.update({'is_active': False})

                product_obj = {'is_active': False,
                               'is_discount': is_discount,
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
                               'subcategory': url_obj,
                               'style': 'feminine'
                               }
                product_list.append(product_obj)
            else:
                print('duplicated')
        except:
            print('error occured')
            pass
    return product_list, duplicate_check_list


def get_dottie():
    obj = HomepageCrawler()
    url_list = ['ao-thun-classic', 'ao-so-mi-ao-kieu-classic', 'ao-khoac-classic',
                'chan-vay-classic', 'jeans-denim', 'vay-dam-classic', 'quan-classic', 'phu-kien-classic']
    product_list = []
    duplicate_check_list = []
    for url_obj in url_list:
        i = 1
        while True:
            url = "https://dottie.vn/collections/" + url_obj + '?page='+str(i)
            print(url)
            response = obj.request_url(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            product_source_list = soup.find('ul', class_='page-group').find_all('li', class_='product')
            if (len(product_source_list) == 0):
                break
            product_sub_list, duplicate_check_list = get_product_sub_list(
                product_source_list, obj, url_obj, duplicate_check_list)
            product_list = product_list + product_sub_list
            i += 1
    return product_list
