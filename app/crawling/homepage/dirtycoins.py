import requests
import json
from random import choice
from bs4 import BeautifulSoup
import csv
import re
from decimal import Decimal

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


def get_cleaned_price(price):
    return int(price)


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


def get_option_from_script(script_list):
    option_json = None
    for script in script_list:
        try:
            script = script.string.replace("'", '"')
            option_string = re.search(r'(?<=product:).*', script)
            option_string = option_string.group().replace('});', '').replace(
                '\n', '').replace('product,', '').strip()[:-1]
            option_json = option_string
            break
        except:
            pass
    return option_json

# In[53]:


def get_product_sub_list(products_soup, obj, sub_cat, duplicate_check_list):
    store = 294
    product_list = []
    for ps in products_soup:
        is_active = False
        product_link = 'https://dirtycoins.vn' + ps.find('div', class_='product-img').find('a').get('href')
        print(product_link)
        response = obj.request_url(product_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_list = soup.find_all('script')
        option_json = get_option_from_script(script_list)
        option_json = json.loads(option_json)
        name = option_json['name']
        created_at = option_json['published_on'].replace('Z', '')

        product_thumbnail_image = "http:"+ps.find('div', class_='product-img').find('img').get('src').replace('large',
                                                                                                              'medium')
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

        description = soup.find('div', class_='product-detail-content')
        if description:
            description = description.text
        else:
            description = ''

        product_image_list = []
        product_images = soup.find_all('li', class_='product-thumb')
        for product_image in product_images:
            source = product_image.find('img').get('src')
            product_image = get_product_image_dict(source)
            product_image_list.append(product_image)

            #     product options
        shopee_size_list = []
        shopee_color_list = []
        product_option_list = []
        stock = 99999
        if option_json:
            stock = 0
            for product_option in option_json['variants']:
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

        print('size ', shopee_size_list, '\ncolor ', shopee_color_list, '\n')
        product_obj = {'is_active': is_active,
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
                       'subcategory': sub_cat,
                       'style': 'street'
                       }
        product_list.append(product_obj)
    return product_list, duplicate_check_list


def get_dirtycoins():
    obj = HomepageCrawler()
    url_list = [
        't-shirts-polos', 'longsleeves',
        'shirts', 'sweaters', 'hoodies', 'jackets', 'pants', 'shorts-1',
        'caps-hats',
        'wallets-1', 'masks', 'backpacks', 'crossbody-bags', 'messenger-bags', 'shoulder-bags',
        'waistbags', ]
    product_list = []
    duplicate_check_list = []
    for url_obj in url_list:
        i = 1
        while True:
            url = "https://dirtycoins.vn/" + url_obj + '?page='+str(i)
            print(url)
            response = obj.request_url(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            products_soup = soup.find('body').find_all('div', class_='single-product')
            if (len(products_soup) == 0):
                break
            product_sub_list, duplicate_check_list = get_product_sub_list(products_soup,
                                                                          obj, url_obj,
                                                                          duplicate_check_list)
            product_list = product_list + product_sub_list
            i += 1
    return product_list
