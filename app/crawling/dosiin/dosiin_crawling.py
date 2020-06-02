#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
from random import choice
from bs4 import BeautifulSoup
import csv


_user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
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


def get_product_image_dict(source):
    product_image = {
        'source': source,
        'source_thumb': source,
        'post_image_type': 'P'
    }
    return product_image


def clear_text(text):
    text = text.lower().replace('\n', '').replace(' ', '').strip()
    return text


# In[41]:


store_list = []


def get_product_sub_list(obj, products_soup, category_obj, sub_cat_obj):
    product_list = []
    for ps in products_soup:
        product_link = ps.find('div', class_='grid-images').find('a').get('href')
        print(product_link)
        response = obj.request_url(product_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = ps.find('a', class_='product-title').text
        store_name = soup.find('a', class_='product_company').get(
            'href').replace('https://dosi-in.com/', '').replace('/', '')

        description = soup.find('meta', itemprop="description").get('content')

        is_discount = False
        discount_rate = None
        discount_price_soup = soup.find('span', class_='list-price')
        price = soup.find('span', class_='price-num').text
        if (discount_price_soup):
            original_price = discount_price_soup.find(class_='strike').text
            original_price = get_cleaned_price(original_price)
            discount_price = get_cleaned_price(price)
            is_discount = True
            discount_rate = soup.find('div', class_='discount-label').text.replace('-', '').replace('%', '')
            discount_rate = clear_text(discount_rate)
        else:
            discount_price = None
            original_price = get_cleaned_price(price)

        product_images = soup.find('div', class_='ty-product-img cm-preview-wrapper').find_all('img', class_='pict')
        product_image_list = []
        product_thumbnail_image = ''
        for i, product_image in enumerate(product_images):
            if (i == 0):
                product_thumbnail_image = product_image.get('src').replace('.webp', '')
            product_image = get_product_image_dict(product_image.get('src').replace('.webp', ''))
            product_image_list.append(product_image)
        product_option_list = []
        shopee_size_list = []
        product_sizes = soup.find_all('label', class_='dosi_option_size')
        total_stock = 99999
        for product_size in product_sizes:
            display_name = clear_text(product_size.text)
            shopee_size_list.append({'display_name': display_name})
            option_name = display_name
            product_option_obj = {
                'is_active': True,
                'name': option_name,
                'original_price': original_price,
                'discount_price': discount_price,
                'currency': 'VND',
                'stock': 99999,
                'size': display_name}
            product_option_list.append(product_option_obj)
        product_obj = {'is_active': False,
                       'is_discount': is_discount,
                       'current_review_rating': 0,
                       'product_source': 'DOSIIN',
                       'product_link': product_link,
                       'store_name': store_name,
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
                       'stock': total_stock,
                       'shopee_size': shopee_size_list,
                       'shopee_color': [],
                       'shopee_category': [],
                       'size_chart': None,
                       'productOption': product_option_list,
                       'style': 'street',
                       'category': category_obj,
                       'subcategory': sub_cat_obj
                       }
        product_list.append(product_obj)
    return product_list


def get_dosiin():
    obj = HomepageCrawler()
    category_list = ['top', 'outer', 'bottom', 'bag', 'sneaker', 'headwear', 'acc', 'nu', 'nam']
    sub_category = {'top': ['sleeveless', 'short-sleeve', 'long-sleeve', 'long-sleeve-vi', 'hoodie-hood-zipup', 'shirts-blouses', 'pike-polo', 'ao-thun-basic', ],
                    'outer': [], 'bottom': [], 'bag': [], 'sneaker': [], 'headwear': [], 'acc': [], 'nu': [], 'nam': []}
    product_list = []
    for category_obj in category_list:
        for sub_cat_obj in sub_category[category_obj]:
            i = 1
            while True:
                url = "https://dosi-in.com/" + sub_cat_obj + '/page-'+str(i)+'/'
                print(url)
                response = obj.request_url(url)
                if (not response):
                    break
                soup = BeautifulSoup(response.text, 'html.parser')
                products_source = soup.find_all('div', class_='grid_item')
                product_sub_list = get_product_sub_list(obj, products_source, category_obj, sub_cat_obj)
                length = len(products_source)
                product_list = product_list + product_sub_list
                i += 1
    return product_list


# In[ ]:
