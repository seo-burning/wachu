import os_setup
import threading
import os

import requests
import json
import time
import datetime
import pytz
from random import choice
from django.db.models import Q
import multiprocessing as mp
from utils.slack import slack_notify
from product.models import Product, ShopeeRating, ProductImage, ShopeeCategory,\
    ProductSize, ProductColor, ProductExtraOption, ProductOption, ProductPattern,\
    ShopeeColor, ShopeeSize, SourceExtraOption
from helper.get_proxy_session import get_session
from helper.clean_text import get_cleaned_text_from_color,\
    get_cleaned_text, get_cleaned_text_from_pattern, \
    get_cleaned_text_from_category, get_cleaned_text_from_size
from django.shortcuts import get_object_or_404
from store.models import Store, StorePost

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


class ShopeeScraper:
    def __init__(self, user_agents=None, proxy=None):
        self.user_agents = user_agents
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.__random_agent(),
                                     'X-Requested-With': 'XMLHttpRequest',
                                     })
        self.proxies = []
        self.session_refresh_count = 0

    def change_session(self):
        if self.session_refresh_count > 5:
            new_session, self.proxies = get_session('new')
            self.session_refresh_count = 0
        else:
            new_session, self.proxies = get_session(proxies=self.proxies)
        self.session = new_session
        self.session_refresh_count += 1
        return new_session

    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(_user_agents)

    def __request_url(self, store_id, limit='100', newest='0'):
        try:
            response = self.session.get('https://shopee.vn/api/v2/search_items/?by=pop&limit={limit}&match_id={store_id}&newest={newest}&order=desc&page_type=shop&shop_categoryids=&version=2'
                                        .format(limit=limit, store_id=store_id, newest=newest),
                                        headers={'User-Agent': choice(_user_agents),
                                                 'X-Requested-With': 'XMLHttpRequest',
                                                 'Referer': 'https://shopee.vn/shop/{store_id}/search?shopCollection='.format(store_id=store_id),
                                                 }, timeout=20)
            # response.raise_for_status()
        except requests.HTTPError as e:
            print(e)
            pass
        except requests.RequestException:
            print(requests.RequestException)
            pass
        else:
            return response

    def __request_url_item(self, store_id, item_id):
        try:
            response = self.session.get("https://shopee.vn/api/v2/item/get?itemid={item_id}&shopid={store_id}"
                                        .format(item_id=item_id, store_id=store_id), headers={'User-Agent': choice(_user_agents),
                                                                                              'X-Requested-With': 'XMLHttpRequest',
                                                                                              'Referer': 'https://shopee.vn/shop/' +
                                                                                              str(store_id) +
                                                                                              '/search?shopCollection=',
                                                                                              }, timeout=20)
            response.raise_for_status()
        except requests.HTTPError as e:
            print(e)
            pass
        except requests.RequestException:
            print(requests.RequestException)
            pass
        else:
            return response

    def __update_category(self, obj_product, categories):
        for category in categories:
            if category:
                obj_cat, is_created = ShopeeCategory.objects.get_or_create(catid=int(category['catid']),
                                                                           display_name=category['display_name'])
                obj_product.shopee_category.add(obj_cat)
                obj_cat.no_sub = category['no_sub']
                obj_cat.is_valid = category['no_sub']
                obj_cat.is_default_subcat = category['is_default_subcat']
                obj_cat.save()
                # is_valid -> 최하위 카테고리 & 분류 된 상태
                if obj_cat.is_valid:
                    if obj_cat.category:
                        obj_product.category = obj_cat.category
                    if obj_cat.sub_category:
                        obj_product.sub_category = obj_cat.sub_category

        if obj_product.sub_category is None:
            obj_product.validation = 'R'  # 카테고리 정상 분류시 Review 로 표시

    def __update_rating(self, obj_product, data, view_count=0):
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
            obj_extra_option, is_created = SourceExtraOption.objects.get_or_create(
                name=option_string, source=source, source_thumb=source_thumb, variation_group=variation_group)
            obj_product.source_extra_option.add(obj_extra_option)

    def __update_size(self, obj_product, options):
        for option in options:
            cleaned_text = get_cleaned_text(option)
            cleaned_text = get_cleaned_text_from_category(
                get_cleaned_text_from_pattern(get_cleaned_text_from_color(cleaned_text)))
            obj_size, is_created = ShopeeSize.objects.get_or_create(
                display_name=cleaned_text)
            obj_product.shopee_size.add(obj_size)
        for size_obj in obj_product.shopee_size.all():
            if size_obj.size:
                obj_product.size.add(size_obj.size)
            else:                # 사이즈 정보 중 없는 정보가 있으면 R로 변경
                obj_product.validation = 'R'

    def __update_color(self, obj_product, options):
        for option in options:
            cleaned_text = get_cleaned_text(option)
            cleaned_text = get_cleaned_text_from_category(
                get_cleaned_text_from_pattern(get_cleaned_text_from_size(cleaned_text)))
            obj_color, is_created = ShopeeColor.objects.get_or_create(
                display_name=cleaned_text)
            obj_product.shopee_color.add(obj_color)
        for color_obj in obj_product.shopee_color.all():
            if color_obj.color:
                obj_product.color.add(color_obj.color)
            else:                # 사이즈 정보 중 없는 정보가 있으면 R로 변경
                obj_product.validation = 'R'

    def __update_product_option(self, obj_product, option_list,
                                color_index, size_index, has_extra_options):
        free_size_obj = ProductSize.objects.get(name='free')
        u_color_obj = ProductColor.objects.get(name='undefined')
        u_size_obj = ProductSize.objects.get(name='undefined')
        # 옵션이 없는 경우 FREE SIZE OPTION 생성
        if len(option_list) == 0:
            obj_option, is_created = ProductOption.objects.get_or_create(
                product=obj_product, shopee_item_id=obj_product.shopee_item_id)
            obj_option.stock = obj_product.stock
            if obj_product.stock > 0:
                obj_option.is_active = True
                obj_product.is_active = True
                obj_product.validation = 'V'
            else:
                obj_option.is_active = False
            obj_option.original_price = obj_product.original_price
            obj_option.discount_price = obj_product.discount_price
            obj_option.currency = obj_product.currency
            obj_option.size = free_size_obj
            obj_option.save()
        else:
            not_valid_information = False
            for option in option_list:
                obj_option, is_created = ProductOption.objects.get_or_create(
                    product=obj_product,
                    shopee_item_id=option['modelid'])
                if is_created:
                    # 옵션 생성 후에는 기본 옵션 정보 선택이 필요.
                    if color_index is None and size_index is None:
                        if len(option_list) == 1:
                            if option['name'] == '':
                                obj_option.name = 'default option(ONE SIZE)'
                            else:
                                obj_option.name = option['name']
                            obj_option.size = free_size_obj
                            obj_option.color = u_color_obj
                        else:
                            not_valid_information = True
                            break
                    else:
                        obj_option.name = option['name']
                        splited_list = option['name'].lower().split(',')
                        if color_index != None:
                            cleaned_text = get_cleaned_text(splited_list[color_index])
                            cleaned_text = get_cleaned_text_from_category(
                                get_cleaned_text_from_pattern(get_cleaned_text_from_size(cleaned_text)))
                            obj_color, is_created = ShopeeColor.objects.get_or_create(
                                display_name=get_cleaned_text(cleaned_text))
                            if obj_color.color:
                                obj_option.color = obj_color.color
                            else:
                                obj_product.validation = 'R'
                                not_valid_information = True
                                break
                        else:
                            obj_option.color = u_color_obj

                        if size_index != None:
                            cleaned_text = get_cleaned_text(splited_list[size_index])
                            cleaned_text = get_cleaned_text_from_category(
                                get_cleaned_text_from_pattern(get_cleaned_text_from_color(cleaned_text)))
                            obj_size, is_created = ShopeeSize.objects.get_or_create(
                                display_name=cleaned_text)
                            if obj_size.size:
                                obj_option.size = obj_size.size
                            else:
                                obj_product.validation = 'R'
                                not_valid_information = True
                                break
                        else:
                            obj_option.size = u_size_obj
                obj_option.is_active = option['status']
                if option['price_before_discount'] > 0:
                    obj_option.original_price = option['price_before_discount'] / 100000
                    obj_option.discount_price = option['price'] / 100000
                else:
                    obj_option.original_price = option['price'] / 100000
                obj_option.currency = option['currency']
                obj_option.stock = option['stock']
                if option['stock'] == 0:
                    obj_option.is_active = False
                obj_option.shopee_sold_count = option['sold']
                try:
                    obj_option.save()
                except:
                    not_valid_information = True

            if has_extra_options or not_valid_information:
                for option in option_list:
                    obj_option, is_created = ProductOption.objects.get_or_create(
                        product=obj_product, shopee_item_id=option['modelid'])
                    obj_option.name = option['name']
                    obj_option.extra_option = option['name']
                    if len(option_list) == 1 and option['name'] == '':
                        obj_option.name = obj_product.name
                        obj_option.extra_option = obj_product.name
                    obj_option.size = u_size_obj
                    obj_option.color = u_color_obj
                    obj_option.is_active = option['status']
                    if option['price_before_discount'] > 0:
                        obj_option.original_price = option['price_before_discount'] / 100000
                        obj_option.discount_price = option['price'] / 100000
                    else:
                        obj_option.original_price = option['price'] / 100000
                    obj_option.currency = option['currency']
                    obj_option.stock = option['stock']
                    if option['stock'] == 0:
                        obj_option.is_active = False
                    obj_option.shopee_sold_count = option['sold']
                    try:
                        obj_option.save()
                    except:
                        obj_product.validation = 'R'

    def __update_price(self, obj_product, data):
        if data['show_discount'] == 0:
            obj_product.is_discount = False
            obj_product.original_price = data['price'] / 100000
            obj_product.discount_price = 0
            obj_product.discount_rate = 0
            obj_product.currency = data['currency']
        else:
            obj_product.is_discount = True
            # price_max_before_discount #price_before_discount
            obj_product.original_price = data['price_before_discount'] / 100000
            obj_product.discount_price = data['price'] / 100000
            obj_product.discount_rate = data['show_discount']
            obj_product.currency = data['currency']
            if (obj_product.original_price == 0 or obj_product.discount_price == 0):
                slack_notify('something wrong with ' + str(obj_product.pk))
        if (data['show_free_shipping']):
            obj_product.is_free_ship = data['show_free_shipping']
            obj_product.shipping_price = 0
        else:
            obj_product.shipping_price = None

    def __update_pattern(self, obj_product):
        pattern_list = ProductPattern.objects.all()
        for pattern_obj in pattern_list:
            name_string = get_cleaned_text(obj_product.name)
            if get_cleaned_text(pattern_obj.name) in name_string or get_cleaned_text(pattern_obj.display_name) in name_string:
                obj_product.pattern.add(pattern_obj)

    def __update_images(self, obj_product, data, is_created=True):
        obj_product.product_thumbnail_image = 'https://cf.shopee.vn/file/' + \
            data['image'] + '_tn'
        if (is_created == False):
            previous_images = ProductImage.objects.filter(product=obj_product)
            for previous_image in previous_images:
                previous_image.delete()
        for product_image in data['images']:
            obj_image, image_is_created = ProductImage.objects.get_or_create(
                source='https://cf.shopee.vn/file/' + product_image,
                source_thumb='https://cf.shopee.vn/file/' + product_image+'_tn',
                product=obj_product,
                post_image_type='P')

    def get_or_create_product(self, store_obj, itemid, view_count=None):
        shopid = store_obj.shopee_numeric_id
        # 0. 상품 생성 및 호출
        obj_product, is_created = Product.objects.get_or_create(
            shopee_item_id=itemid, store=store_obj)
        # print('https://dabivn.com/admin/product/product/'+str(obj_product.pk))
        # 0. 상품 json load
        data = self.__request_url_item(shopid, itemid).json()['item']
        print('.', end='')
        # 1. 상품 삭제 확인
        if data == None:
            print('d', end='')
            obj_product.is_active = False
            obj_product.validation = 'D'
            obj_product.name = '[DELETED FROM SOURCE PAGE]' + obj_product.name
            obj_product.save()
        else:
            # TODO 재고 재 생성 확인을 해야함.
            # 2. 신규 생성 상품 처리
            color_index = None
            size_index = None
            has_extra_options = False
            if is_created:
                # 2. 기본 정보 업데이트 (상품 링크 / 상품 생성 시간 / 상품 분류 / 이름 / 이미지)
                print('n', end='')
                obj_product.validation = 'V'
                self.__update_category(obj_product, data['categories'])
                obj_product.product_link = store_obj.shopee_url + '/' + str(itemid)
                obj_product.created_at = datetime.datetime.fromtimestamp(
                    int(data['ctime']), pytz.UTC)
                obj_product.product_source = 'SHOPEE'
                obj_product.name = data['name']
                obj_product.description = data['description']
                # image
                self.__update_images(obj_product, data, is_created)
                # 2. 상품 사이즈 / 컬러 정보 업데이트
                if (data['size_chart'] != None):
                    obj_product.size_chart = 'https://cf.shopee.vn/file/' + data['size_chart']
                for i, variation in enumerate(data['tier_variations']):
                    variation_name = variation['name'].replace(' ', '').replace(':', '').lower().strip()
                    if 'size' in variation_name or 'kích' in variation_name or 'kich' in variation_name:
                        self.__update_size(obj_product, variation['options'])
                        size_index = i
                    elif 'màu' in variation_name or 'color' in variation_name or 'mau' in variation_name:
                        self.__update_color(obj_product, variation['options'])
                        color_index = i
                    else:
                        self.__update_extra_options(obj_product, variation)
                        has_extra_options = True
                if obj_product.size.count() == 0:
                    self.__update_size(obj_product, ['free'])
                # 2. 패턴 추가
                self.__update_pattern(obj_product)

            if (obj_product.product_thumbnail_image != 'https://cf.shopee.vn/file/' +
                    data['image'] + '_tn'):
                print('recreate images', end='')
                self.__update_images(obj_product, data, False)
            # 3. 기존 / 신규 상품 업데이트
            # 3. 가격 및 레이팅 업데이트
            obj_product.updated_at = datetime.datetime.now()
            self.__update_price(obj_product, data)
            if view_count:
                self.__update_rating(obj_product, data, view_count)

            # 3. 재고 및 품절 처리
            obj_product.stock = data['stock']
            if (obj_product.stock == 0):
                obj_product.is_active = False
                obj_product.stock_available = False
            else:
                obj_product.stock_available = True

            # 4. 옵션 생성 및 업데이트
            self.__update_product_option(obj_product, data['models'], color_index, size_index, has_extra_options)
            obj_product.save()

            # 5. 생성 후 최종 검증
            if is_created:
                obj_product.is_active = False
                obj_product.save()
        return obj_product

    def search_store(self, store_obj):
        i = 0
        pk = 0
        list_length = 100
        store_id = store_obj.insta_id
        while list_length == 100:
            try:
                error_try_count = 0
                while True or error_try_count > 5:
                    try:
                        response = self.__request_url(store_id=store_obj.shopee_numeric_id,
                                                      limit=list_length, newest=i*100)
                        product_list = response.json()['items']
                        break
                    except:
                        error_try_count += 1
                        # if error_try_count > 5 and error_try_count % 2 == 0:
                        #     new_session = self.change_session()
                        # else:
                        print('R', end='')
                        # continue
                        # print('E', end='')
                for j, product in enumerate(product_list):
                    error_try_count = 0
                    while True or error_try_count > 10:
                        try:
                            product_obj = self.get_or_create_product(
                                store_obj, product['itemid'], product['view_count'])
                            break
                        except:
                            print('e', end='')
                            new_session = self.change_session()
                            error_try_count += 1
                    if (i == 0 and j == 0):
                        store_obj.recent_post_1 = product_obj.product_thumbnail_image
                    elif (i == 0 and j == 1):
                        store_obj.recent_post_2 = product_obj.product_thumbnail_image
                    elif (i == 0 and j == 2):
                        store_obj.recent_post_3 = product_obj.product_thumbnail_image
                    store_obj.save()
                    pk += 1
                list_length = len(product_list)
                i = i+1
            except:
                print('\nERROR\n')
                slack_notify('Failed to get product list from {} {} ~ {}'.format(store_obj.insta_id, i*100, (i+1)*100))
        return pk


def update_shopee(start_index=0, end_index=None, reverse=False):
    obj = ShopeeScraper()
    store_list = Store.objects.filter(store_type='IS').filter(is_active=True)[start_index:end_index]
    for i, store_obj in enumerate(store_list):
        print("\n#" + str(i) + ' update ' + str(store_obj))
        updated = obj.search_store(store_obj)


def validate_shopee(start_index=0, end_index=None, reverse=False):
    obj = ShopeeScraper()
    store_list = Store.objects.filter(store_type='IS').filter(is_active=True)[start_index:end_index]
    for i, store_obj in enumerate(store_list):
        print("\n#" + str(i) + ' update ' + str(store_obj))
        product_list = Product.objects.filter(is_active=True, store=store_obj, product_source='SHOPEE')
        for product_obj in product_list:
            error_try_count = 0
            while True or error_try_count > 20:
                try:
                    obj.get_or_create_product(store_obj, product_obj.shopee_item_id)
                    print(product_obj.shopee_item_id)
                    break
                except:
                    obj.change_session()
                    error_try_count += 1


def multi(product_obj):
    obj = ShopeeScraper()
    store = product_obj.store
    if store:
        print('update ' + 'https://dabivn.com/admin/product/product/' + str(product_obj.pk))
        obj.get_or_create_product(store, product_obj.shopee_item_id)


def du_check(po):
    options = po.product_options
    for option in options.all():
        print('.', end='')
        option_num = options.filter(product=po, size=option.size, color=option.color, extra_option=option.extra_option)
        if len(option_num) > 1:
            print('d', end='')
            po.validation = 'R'
            po.is_active = False
            break


if __name__ == '__main__':
    # pool = mp.Pool(processes=64)
    # store_list = Store.objects.filter(is_active=True, store_type='IS')
    # obj = ShopeeScraper()
    # pool.map(obj.search_store, store_list)
    # pool.close()
    # obj = ShopeeScraper()
    # obj.search_store(Store.objects.get(insta_id='xinh_store'))
    validate_shopee(125)
