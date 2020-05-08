
import requests
import json
import sys
import os
import django
import time
import datetime
import pytz
from random import choice
from django.db.models import Q
import os_setup
import multiprocessing as mp
from utils.slack import slack_notify, slack_upload_file
from product.models import Product, ShopeeRating, ProductImage, ShopeeCategory, ProductSize, ProductColor, ProductExtraOption, ProductOption, ShopeeColor, ShopeeSize
from store.models import Store, StorePost
PROJECT_ROOT = os.getcwd()
sys.path.append(os.path.dirname(PROJECT_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.prod")
django.setup()


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


class ShopeeScraper:
    def __init__(self, user_agents=None, proxy=None):
        self.user_agents = user_agents
        self.proxy = proxy

    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(_user_agents)

    def __random_proxies(self):
        if self.proxy and isinstance(self.proxy, list):
            print('execute')
            return choice(self.proxy)
        proxies = get_proxies()
        return random.sample(get_proxies(), 1)[0]

    def __request_url(self, store_id, limit='100', newest='0'):
        try:
            response = requests.get('https://shopee.vn/api/v2/search_items/?by=pop&limit={limit}&match_id={store_id}&newest={newest}&order=desc&page_type=shop&shop_categoryids=&version=2'.format(limit=limit, store_id=store_id, newest=newest),
                                    headers={'User-Agent': self.__random_agent(),
                                             'X-Requested-With': 'XMLHttpRequest',
                                             'Referer': 'https://shopee.vn/shop/{store_id}/search?shopCollection='.format(store_id=store_id),
                                             },
                                    proxies={'http': self.proxy, 'https': self.proxy})
            response.raise_for_status()
        except requests.HTTPError as e:
            print(e)
            pass
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response

    def request_url_item(self, store_id, item_id):
        try:
            response = requests.get("https://shopee.vn/api/v2/item/get?itemid={item_id}&shopid={store_id}".format(item_id=item_id, store_id=store_id), headers={'User-Agent': self.__random_agent(),
                                                                                                                                                                'X-Requested-With': 'XMLHttpRequest',
                                                                                                                                                                'Referer': 'https://shopee.vn/shop/'+str(store_id)+'/search?shopCollection=',
                                                                                                                                                                },
                                    proxies={'http': self.proxy, 'https': self.proxy})
            response.raise_for_status()
        except requests.HTTPError as e:
            print(e)
            pass
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response

    def __request_url_item(self, store_id, item_id):
        try:
            response = requests.get("https://shopee.vn/api/v2/item/get?itemid={item_id}&shopid={store_id}".format(item_id=item_id, store_id=store_id), headers={'User-Agent': self.__random_agent(),
                                                                                                                                                                'X-Requested-With': 'XMLHttpRequest',
                                                                                                                                                                'Referer': 'https://shopee.vn/shop/'+str(store_id)+'/search?shopCollection=',
                                                                                                                                                                },
                                    proxies={'http': self.proxy, 'https': self.proxy})
            response.raise_for_status()
        except requests.HTTPError as e:
            print(e)
            pass
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response

    def __update_category(self, obj_product, categories):
        for category in categories:
            obj_cat, is_created = ShopeeCategory.objects.get_or_create(catid=int(category['catid']),
                                                                       display_name=category['display_name'])
            obj_product.shopee_category.add(obj_cat)
            obj_cat.no_sub = category['no_sub']
            obj_cat.is_valid = category['no_sub']
            obj_cat.is_default_subcat = category['is_default_subcat']
            obj_cat.save()
            if obj_cat.is_valid:
                print(obj_cat.display_name)
                if obj_cat.category:
                    obj_product.category = obj_cat.category
                    print('category added')
                if obj_cat.sub_category:
                    obj_product.sub_category = obj_cat.sub_category
                    print('sub-category added')
        if obj_product.sub_category:
            obj_product.is_active = True
        else:
            obj_product.is_active = False
        obj_product.save()
        return obj_product.is_active

    def __update_extra_options(self, obj_product, variation):
        options = variation['options']
        images = variation['images']
        variation_group = variation['name']
        for key, option in enumerate(options):
            option_string = option.lower().strip()
            try:
                source = 'https://cf.shopee.vn/file/' + \
                    variation['images'][key]
                source_thumb = 'https://cf.shopee.vn/file/' + \
                    variation['images'][key]+'_tn'
            except:
                source = None
                source_thumb = None
            obj_extra_option, is_created = ProductExtraOption.objects.get_or_create(
                name=option_string, source=source, source_thumb=source_thumb, variation_group=variation_group)
            obj_product.extra_option.add(obj_extra_option)
            print(option_string)
        obj_product.save()

    def __update_size(self, obj_product, options):
        print(options)
        obj_product.size.clear()
        obj_product.shopee_size.clear()
        for option in options:
            option_string = option.lower().replace('size', '').replace(' ', '').strip()
            obj_size, is_created = ShopeeSize.objects.get_or_create(
                display_name=option_string)
            obj_product.shopee_size.add(obj_size)
        for size_obj in obj_product.shopee_size.all():
            if size_obj.size:
                # print("exist : {} => {}".format(size_obj.display_name, size_obj.size))
                obj_product.size.add(size_obj.size)
            else:
                # print("not exist : {}".format(size_obj.display_name))
                pass
        obj_product.save()

    def __update_color(self, obj_product, options):
        obj_product.color.clear()
        obj_product.shopee_color.clear()
        for option in options:
            option_string = option.lower().replace('màu', '').replace(
                'mau', '').replace('color', '').strip()
            obj_color, is_created = ShopeeColor.objects.get_or_create(
                display_name=option_string)
            obj_product.shopee_color.add(obj_color)
        for color_obj in obj_product.shopee_color.all():
            if color_obj.color:
                # print("exist : {} => {}".format(color_obj.display_name, color_obj.color))
                obj_product.color.add(color_obj.color)
            else:
                # print("not exist : {}".format(color_obj.display_name))
                pass
        obj_product.save()

    def __update_rating(self, obj_product, data, view_count):
        obj_rating, is_created = ShopeeRating.objects.get_or_create(
            product=obj_product)
        if data['liked_count']:
            obj_rating.shopee_liked_count = data['liked_count']
        if data['historical_sold']:
            obj_rating.shopee_sold_count = data['historical_sold']
        obj_rating.shopee_view_count = view_count
        if data['item_rating']['rating_star']:
            obj_rating.shopee_rating_star = data['item_rating']['rating_star']
        if data['item_rating']['rating_count']:
            obj_rating.shopee_5_star_count = data['item_rating']['rating_count'][0]
            obj_rating.shopee_4_star_count = data['item_rating']['rating_count'][1]
            obj_rating.shopee_3_star_count = data['item_rating']['rating_count'][2]
            obj_rating.shopee_2_star_count = data['item_rating']['rating_count'][3]
            obj_rating.shopee_1_star_count = data['item_rating']['rating_count'][4]
            obj_rating.shopee_review_count = data['item_rating']['rating_count'][0]+data['item_rating']['rating_count'][1] + \
                data['item_rating']['rating_count'][2]+data['item_rating']['rating_count'][3] + \
                data['item_rating']['rating_count'][4]
        obj_rating.save()

    def __update_price(self, obj_product, data):
        if data['show_discount'] == 0:
            obj_product.original_price = data['price'] / 100000
            obj_product.discount_rate = data['show_discount']
            obj_product.currency = data['currency']
        else:
            obj_product.is_discount = True
            # price_max_before_discount #price_before_discount
            obj_product.original_price = data['price_before_discount'] / 100000
            obj_product.discount_price = data['price'] / 100000
            obj_product.discount_rate = data['show_discount']
            obj_product.currency = data['currency']
            if (obj_product.original_price == 0 or obj_product.discount_price == 0):
                time.sleep(10000)
        obj_product.save()

    def __update_product_option(self, obj_product, option_list):
        for option in option_list:
            obj_option, is_created = ProductOption.objects.get_or_create(
                product=obj_product, shopee_item_id=option['modelid'])
            obj_option.is_active = option['status']
            obj_option.name = option['name']

            if option['price_before_discount'] > 0:
                obj_option.original_price = option['price_before_discount'] / 100000
                obj_option.discount_price = option['price'] / 100000
            else:
                obj_option.original_price = option['price'] / 100000

            obj_option.currency = option['currency']
            obj_option.stock = option['stock']
            obj_option.shopee_sold_count = option['sold']
            obj_option.save()

    def get_or_create_product(self, store_obj, itemid, view_count, created, need_to_update):
        shopid = store_obj.shopee_numeric_id
        obj_product, is_created = Product.objects.get_or_create(
            shopee_item_id=itemid, store=store_obj)
        data = self.__request_url_item(shopid, itemid).json()['item']
        if is_created:
            # print(store_obj.insta_id, itemid)
            is_valid = self.__update_category(obj_product, data['categories'])
            if (is_valid == False):
                need_to_update.append(obj_product.product_link)
            obj_product.product_link = store_obj.shopee_url + '/' + str(itemid)
            obj_product.created_at = datetime.datetime.fromtimestamp(
                int(data['ctime']), pytz.UTC)
            if (data['size_chart'] != None):
                obj_product.size_chart = 'https://cf.shopee.vn/file/' + data['size_chart']
            created.append(obj_product.product_link)
            obj_product.product_source = 'SHOPEE'
            obj_product.name = data['name']
            obj_product.description = data['description']
            # image
            obj_product.product_thumbnail_image = 'https://cf.shopee.vn/file/' + \
                data['image'] + '_tn'
            obj_product.save()
            for product_image in data['images']:
                obj_image, image_is_created = ProductImage.objects.get_or_create(
                    source='https://cf.shopee.vn/file/' + product_image,
                    source_thumb='https://cf.shopee.vn/file/' + product_image+'_tn',
                    product=obj_product,
                    post_image_type='P')

            for variation in data['tier_variations']:
                # print(variation['name'])
                variation_name = variation['name'].lower().strip()
                if variation_name == 'size' or variation_name == 'kích cỡ' or variation_name == 'kích thước':
                    self.__update_size(obj_product, variation['options'])
                elif 'màu' in variation_name or 'color' in variation_name:
                    self.__update_color(obj_product, variation['options'])
                else:
                    self.__update_extra_options(obj_product, variation)

        if data['models']:
            self.__update_product_option(obj_product, data['models'])
        self.__update_price(obj_product, data)
        self.__update_rating(obj_product, data, view_count)
        obj_product.is_free_ship = data['show_free_shipping']
        obj_product.stock = data['stock']
        obj_product.save()
        return obj_product, created, need_to_update

    def search_store(self, store_obj):
        i = 0
        pk = 0
        created = []
        need_to_update = []
        list_length = 100
        store_id = store_obj.insta_id
        while list_length == 100:
            response = self.__request_url(
                store_id=store_obj.shopee_numeric_id, limit=list_length, newest=i*100)
            try:
                product_list = response.json()['items']
                for j, product in enumerate(product_list):
                    # print("{} - #{} product".format(store_id, i*list_length+j+1))
                    try:
                        product_obj, created, need_to_update = self.get_or_create_product(
                            store_obj, product['itemid'], product['view_count'], created, need_to_update)
                    except:
                        slack_notify('error : {} #{} {}'.format(store_id, i, product['itemid']))
                    if (i == 0 and j == 0):
                        store_obj.recent_post_1 = product_obj.product_thumbnail_image
                        # print(store_obj.recent_post_1)
                    elif (i == 0 and j == 1):
                        store_obj.recent_post_2 = product_obj.product_thumbnail_image
                        # print(store_obj.recent_post_2)
                    elif (i == 0 and j == 2):
                        store_obj.recent_post_3 = product_obj.product_thumbnail_image
                        # print(store_obj.recent_post_3)
                    store_obj.save()
                    pk += 1
                list_length = len(product_list)
                i = i+1
            except:
                slack_notify('error : {} #{} {}'.format(store_id, i*100, "fail to get list"))
                i = i+1

        return pk, len(created), len(need_to_update)


def _update_color_size_from_shopee_color_size(product_obj):
    product_obj.color.clear()
    product_obj.size.clear()
    for color_obj in product_obj.shopee_color.all():
        if color_obj.color:
            # print("exist : {} => {}".format(color_obj.display_name, color_obj.color))
            product_obj.color.add(color_obj.color)
        else:
            # print("not exist : {}".format(color_obj.display_name))
            pass
    for size_obj in product_obj.shopee_size.all():
        if size_obj.size:
            # print("exist : {} => {}".format(size_obj.display_name, size_obj.size))
            product_obj.size.add(size_obj.size)
        else:
            # print("not exist : {}".format(size_obj.display_name))
            pass
    product_obj.save()


def update_color_size_from_shopee_color_size():
    # print('Update Color&Size from Shopee Color&Size')
    product_list = Product.objects.filter(product_source='SHOPEE')
    # print(product_list.count())
    # pool = mp.Pool(processes=6)
    # print('Set up Multiprocessing....')
    # pool.map(_update_color_size_from_shopee_color_size, product_list)
    for product_obj in product_list:
        _update_color_size_from_shopee_color_size(product_obj)
    # pool.close()


def _update_product_category_from_shopee(obj_product):
    shopee_category = obj_product.shopee_category
    for obj_cat in shopee_category.all():
        if obj_cat.is_valid:
            # print(obj_cat.display_name)
            if obj_cat.category:
                obj_product.category = obj_cat.category
                # print('category added')
            if obj_cat.sub_category:
                obj_product.sub_category = obj_cat.sub_category
                # print('sub-category added')
    if obj_product.sub_category:
        obj_product.is_active = True
    else:
        obj_product.is_active = False
    obj_product.save()


def update_product_category_from_shopee():
    # print('Update Category from Shopee')
    product_list = Product.objects.filter(product_source='SHOPEE')
    # print(product_list.count())
    for product_obj in product_list:
        _update_product_category_from_shopee(product_obj)


def update_shopee():
    obj = ShopeeScraper()
    store_list = Store.objects.filter(
        Q(store_type='IS') |
        Q(store_type='IFSH') |
        Q(store_type='IF(P)SH') |
        Q(store_type='IS(P)')
    )
    total_updated = 0
    total_created = 0
    total_need_to_update = 0
    file_path = './shopee_result.txt'
    with open(file_path, "w") as f:
        for i, store_obj in enumerate(store_list):
            updated, created, need_to_update = obj.search_store(store_obj)
            result_text = store_obj.insta_id + 'total : ' + str(updated) + '  created : ' + str(created) + \
                '   need to update : '+str(need_to_update) + '\n'
            f.writelines(result_text)
            total_updated += updated
            total_created += created
            total_need_to_update += need_to_update
    slack_notify('>total : ' + str(total_updated) + '  created : ' + str(total_created) +
                 '   need to update : '+str(total_need_to_update) + '\n')
    slack_upload_file(file_path)
    os.remove(file_path)
