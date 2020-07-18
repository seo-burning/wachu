import requests
import json
from random import choice
from bs4 import BeautifulSoup
import csv
import re
from decimal import Decimal
from .get_proxy_session import get_session
_user_agents = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
]

shopee_color_list_duplicate = []
shopee_size_list_duplicate = []
size_option_list = ['xs', 's', 'm', 'l', 'xl', 'free', 'freesize', '25', '26', '27', '28',
                    '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
                    '1', '2', '3', '4', '5', 'lớn', 'nhỏ']


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
        self.session = get_session()

    def __change_session(self):
        i = 1
        while new_session != self.session:
            print('try to get new session #' + str(i))
            new_session = get_session()
            i = i + 1
        self.session = new_session

    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(_user_agents)

    def request_url(self, url):
        try:
            response = self.session.get(url,
                                        headers={'User-Agent': self.__random_agent(),
                                                 'X-Requested-With': 'XMLHttpRequest',
                                                 },)
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


def get_cleaned_price(price, price_divider=100):
    return int(price/price_divider)


def calculate_discount_rate(original_price, discount_price):
    discount_rate = int((1 - Decimal(discount_price)/Decimal(original_price))*100)
    return discount_rate


def get_cleaned_text(text):
    text = text.lower().replace(' ', '').replace('\x08', '').replace('size', '').strip()
    return text


def get_product_image_dict(source):
    product_image = {
        'source': source,
        'source_thumb': source,
        'post_image_type': 'P'
    }
    return product_image


def get_option_from_script(script_list, script_string):
    option_json = None
    for script in script_list:
        try:
            script = script.string
            option_string = re.search(script_string, script)
            option_string = option_string.group().replace('});', '').replace(
                ', onVariantSelected: selectCallback', '').replace('{ product: ', '').strip()
            if option_string[-1:] == ';' or option_string[-1:] == ',':
                option_string = option_string[:-1]
            option_json = option_string
#             print(option_json)
            break
        except:
            pass
    return option_json


def define_type(option_a, option_b):
    option_a = get_cleaned_text(option_a)
    option_b = get_cleaned_text(option_b)

    if option_a in size_option_list:
        size_obj = {'display_name': get_cleaned_text(option_a)}
        color_obj = {'display_name': get_cleaned_text(option_b)}
    elif option_b in size_option_list:
        size_obj = {'display_name': get_cleaned_text(option_b)}
        color_obj = {'display_name': get_cleaned_text(option_a)}
    else:
        size_obj = None
        color_obj = None
    return size_obj, color_obj


def define_type_single(option):
    option = get_cleaned_text(option)
    if option in size_option_list:
        size_obj = {'display_name': get_cleaned_text(option)}
        color_obj = None
    else:
        size_obj = None
        color_obj = {'display_name': get_cleaned_text(option)}
    return size_obj, color_obj


def get_product_obj_from_json(store, style, url_obj,
                              product_link, option_json, option_type, price_divider, image_type):
        #     title / description
    if 'published_on' in option_json:
        created_at = option_json['published_on'].replace('Z', '')
    else:
        created_at = option_json['published_at'].replace('Z', '')

    if 'title' in option_json:
        name = option_json['title']
    elif 'name' in option_json:
        name = option_json['name']

    if 'description' in option_json:
        description = option_json['description']
    elif 'meta_description' in option_json:
        description = option_json['meta_description']

    original_price = get_cleaned_price(option_json['price'], price_divider)
    discount_price = None
    discount_rate = None
    is_discount = False
    if (option_json['compare_at_price_max'] != 0.0) & (option_json['price'] != option_json['compare_at_price_max']):
        is_discount = True
        discount_price = get_cleaned_price(option_json['price'], price_divider)
        original_price = get_cleaned_price(option_json['compare_at_price_max'], price_divider)
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
        if type(source) is dict and 'src' in source:
            source = source['src']
        product_image = get_product_image_dict(source)
        product_image_list.append(product_image)
    product_thumbnail_image = option_json['featured_image']
    if type(product_thumbnail_image) is dict and 'src' in product_thumbnail_image:
        product_thumbnail_image = product_thumbnail_image['src']
    if image_type == 1:
        product_thumbnail_image = product_thumbnail_image.replace(
            '.jpg', '_large.jpg').replace('.jpeg', '_large.jpeg').replace('.png', '_large.png')
    elif image_type == 2:
        product_thumbnail_image = product_thumbnail_image.replace(
            '.net/', '.net/thumb/medium/')
#     product options
    product_option_list = []
    shopee_size_list = []
    shopee_color_list = []
    if option_json:
        stock = 0
        for i, product_option in enumerate(option_json['variants']):
            option1 = product_option['option1']
            option2 = product_option['option2']
            option3 = product_option['option3']
            if option3:
                if option_type == 12:
                    size_obj, color_obj = define_type(option1, option2)
                elif option_type == 13:
                    size_obj, color_obj = define_type(option1, option3)
                elif option_type == 23:
                    size_obj, color_obj = define_type(option2, option3)
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
                'shopee_item_id': i,
                'currency': 'VND',
                'size': size_obj,
                'color': color_obj,
                'stock': option_stock, }
            product_option_list.append(product_option_obj)

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
                   'style': style,
                   'subcategory': str(store)+'-'+url_obj,
                   }
    return product_obj


# In[3]:


def get_product_obj_from_soup(store, style, url_obj, product_link, product_soup):
    is_discount = False
    created_at = None
#     thumbnail
    product_thumbnail_image = "http:" + product_soup.find("img",
                                                          class_="product-image-feature").get('src').replace('grande',
                                                                                                             'large').replace('1024x1024', 'large').replace('master', 'large')

#     title
    name = product_soup.find('h1').text
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
        discount_rate = product_price.find('span', class_='pro-sale').text.replace('-',
                                                                                   '').replace('%', '').replace(' ', '')
    else:
        original_price = product_price.find(
            'span', class_='pro-price').text.replace(',', '').replace('₫', '').replace(' ', '')
        discount_price = None
        discount_rate = None
        is_discount = False

#      stock
    stock = product_soup.find('button', class_='disabled')
    if stock:
        stock = 0
    else:
        stock = 9999
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
                   'shopee_size': [],
                   'shopee_color': [],
                   'shopee_category': [],
                   'size_chart': None,
                   'productOption': [],
                   'style': style,
                   'subcategory': str(store)+'-'+url_obj,
                   }
    return product_obj


def sub_crawler(obj, url, store_pk, style, product_source, url_obj,
                option_type,
                script_string, price_divider, image_type,
                duplicate_check_list,):
    product_list = []
    store = store_pk
    for product_obj in product_source:
        print('.', end='')
        #     link and get json
        product_link_soup = product_obj.find("a", href=True)
        if product_link_soup.get('href') == '/account/login':
            product_link_soup = product_obj.find_all("a", href=True)
            product_link_soup = product_link_soup[1]
        product_link = url + product_link_soup.get('href')
        if product_link not in duplicate_check_list:
            duplicate_check_list.append(product_link)
            response = obj.request_url(product_link)
            product_soup = BeautifulSoup(response.text, 'html.parser')
            try:
                script_list = product_soup.find_all('script')
                option_json = get_option_from_script(script_list, script_string)
                option_json = json.loads(option_json)
                product_obj = get_product_obj_from_json(
                    store, style, url_obj, product_link,
                    option_json, option_type, price_divider, image_type)
            except:
                product_obj = get_product_obj_from_soup(store, style, url_obj, product_link, product_soup)
            product_list.append(product_obj)
        else:
            pass
    return product_list, duplicate_check_list


def homepage_crawler(url, store_pk, style,
                     url_list=['all'],
                     block_name='product-block',
                     option_type=12,
                     script_string=r'(?<=product:).*',
                     price_divider=100, image_type=1):
    obj = HomepageCrawler()
    product_list = []
    duplicate_check_list = []
    for url_obj in url_list:
        i = 1
        while True:
            print(",", end='')
            request_url = url+"/collections/"+url_obj+"?page=" + str(i)
            response = obj.request_url(request_url)
            if response is None:
                break
            soup = BeautifulSoup(response.text, 'html.parser')
            product_source = soup.find_all("div", class_=block_name)
            product_sub_list, duplicate_check_list = sub_crawler(obj,
                                                                 url,
                                                                 store_pk,
                                                                 style,
                                                                 product_source,
                                                                 url_obj,
                                                                 option_type,
                                                                 script_string,
                                                                 price_divider, image_type,
                                                                 duplicate_check_list,
                                                                 )
            product_list = product_list + product_sub_list
            length = len(product_source)
            if length == 0:
                break
            i = i+1
    return product_list
