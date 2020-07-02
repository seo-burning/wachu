

import requests
import json
from random import choice
from bs4 import BeautifulSoup
import csv
import re
# In[3]:


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


def get_cleaned_text(text):
    text = text.replace(' ', '').replace('\x08', '').strip().lower()
    return text


def get_option_from_script(script_list):
    option_json = None
    for script in script_list:
        try:
            script = script.string
            option_string = re.search(r'(?<="product-select",).*', script)
            option_string = option_string.group().replace('});', '').replace(
                ', onVariantSelected: selectCallback', '').replace('{ product: ', '').strip()
            option_json = option_string
        except:
            pass
    return option_json


def define_type(option_a, option_b):
    option_a = get_cleaned_text(option_a)
    option_b = get_cleaned_text(option_b)
    size_option_list = ['xs', 's', 'm', 'l', 'xl', 'free']
    if option_a in size_option_list:
        size_obj = {'display_name': get_cleaned_text(option_a)}
        color_obj = {'display_name': get_cleaned_text(option_b)}
    else:
        size_obj = {'display_name': get_cleaned_text(option_b)}
        color_obj = {'display_name': get_cleaned_text(option_a)}
    return size_obj, color_obj


def define_type_single(option):
    option = get_cleaned_text(option)
    size_option_list = ['xs', 's', 'm', 'l', 'xl', 'free', 'defaulttitle']
    if option in size_option_list:
        size_obj = {'display_name': get_cleaned_text(option)}
        color_obj = None
    else:
        size_obj = None
        color_obj = {'display_name': get_cleaned_text(option)}
    return size_obj, color_obj

# In[32]:


def sub_crawler(obj, product_source):
    obj = HomepageCrawler()
    product_list = []
    store = 293
    for product_obj in product_source:
        is_discount = False
    #     thumbnail / link
        product_link_soup = product_obj.find("a", href=True)
        product_link = "https://hades.vn"+product_link_soup.get('href')
        product_thumbnail_image = "http:"+product_link_soup.find("img", class_="img-loop").get('src').replace('grande',
                                                                                                              'large').replace('large', 'large').replace('medium', 'large')

    #     title
        created_at = None
        response = obj.request_url(product_link)
        product_soup = BeautifulSoup(response.text, 'html.parser')
        name = product_soup.find('h1').text
        description = product_soup.find('div', class_='description-content').find('p')
        if description:
            description = description.text
        else:
            description = ''

    #     product image list
        product_images = product_soup.find_all('img', class_='product-image-feature')
        product_image_list = []
        for product_image_obj in product_images:
            source = "http:" + product_image_obj.get('src')
            product_image = {
                'source': source,
                'source_thumb': source,
                'post_image_type': 'P'
            }
            product_image_list.append(product_image)

    #     product price
        product_price = product_soup.find('div', class_='product-price')
        if product_price.find('span', class_='pro-sale'):
            is_discount = True
            original_price = product_price.find('del').text.replace(',', '').replace('₫', '').replace(' ', '')
            discount_price = product_price.find(
                'span', class_='pro-price').text.replace(',', '').replace('₫', '').replace(' ', '')
            discount_rate = product_price.find(
                'span', class_='pro-sale').text.replace('-', '').replace('%', '').replace(' ', '')
        else:
            original_price = product_price.find(
                'span', class_='pro-price').text.replace(',', '').replace('₫', '').replace(' ', '')
            discount_price = None
            discount_rate = None
            is_discount = False

    #     product stock
        product_stock_soup = product_soup.find('button', class_='disabled add-to-cartProduct')
        if product_stock_soup:
            stock = 0
        else:
            stock = 99999

    #     product options
        script_list = product_soup.find_all('script')
        option_json = get_option_from_script(script_list)
        product_option_list = []
        shopee_size_list = []
        shopee_color_list = []
        stock = 99999
        if option_json:
            option_json = json.loads(option_json)
            stock = 0
            created_at = option_json['published_at'].replace('Z', '')

            for product_option in option_json['variants']:
                # print(product_option)
                option1 = product_option['option1']
                option2 = product_option['option2']
                if option2:
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

        # print(shopee_size_list)
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
    return product_list


def get_hades():
    obj = HomepageCrawler()
#     category_list = ['top','outwear', 'sweater-1', 'bottoms', 'hat']
    i = 1
    product_list = []
    while True:
        url = "https://hades.vn/collections/all?page=" + str(i)
        response = obj.request_url(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        product_source = soup.find_all("div", class_="product-block")
        product_sub_list = sub_crawler(obj, product_source)
        product_list = product_list + product_sub_list
        length = len(product_source)
        # print(length)
        if length == 0:
            break
        i = i+1
    return product_list
