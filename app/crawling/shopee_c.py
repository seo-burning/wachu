
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
from product.models import Product, ShopeeRating, ProductImage, ShopeeCategory, ProductSize, ProductColor, ProductExtraOption, ProductOption, ShopeeColor, ShopeeSize, SourceExtraOption
from store.models import Store, StorePost
from django.shortcuts import get_object_or_404

from manual_update import make_product_options_from_product


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


class ShopeeScraper:
    def __init__(self, user_agents=None, proxy=None):
        self.user_agents = user_agents
        self.proxy = proxy

    def __request_url(self, store_id, limit='100', newest='0'):
        try:
            response = requests.get('https://shopee.vn/api/v2/search_items/?by=pop&limit={limit}&match_id={store_id}&newest={newest}&order=desc&page_type=shop&shop_categoryids=&version=2'
                                    .format(limit=limit, store_id=store_id, newest=newest),
                                    headers={'User-Agent': choice(_user_agents),
                                             'X-Requested-With': 'XMLHttpRequest',
                                             'Referer': 'https://shopee.vn/shop/{store_id}/search?shopCollection='.format(store_id=store_id),
                                             },)
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
            response = requests.get("https://shopee.vn/api/v2/item/get?itemid={item_id}&shopid={store_id}"
                                    .format(item_id=item_id, store_id=store_id), headers={'User-Agent': choice(_user_agents),
                                                                                          'X-Requested-With': 'XMLHttpRequest',
                                                                                          'Referer': 'https://shopee.vn/shop/'+str(store_id)+'/search?shopCollection=',
                                                                                          },)
            response.raise_for_status()
        except requests.HTTPError as e:
            print(e)
            pass
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response

    def __get_cleaned_text(self, text):
        text = text.lower().replace(' ', '').replace('(', '').replace(')', '').replace(':', '').replace('eodưới', '').replace(
            'dưới', '').replace('dưới', '').replace('<', '').replace('kg', '').replace('size', '').replace('szie', '').replace(
                'sz', '').replace('mau', '').replace('màu', '').replace('color', '').strip()
        return text

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
        return obj_product.is_active

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
            obj_size, is_created = ShopeeSize.objects.get_or_create(
                display_name=self.__get_cleaned_text(option))
            obj_product.shopee_size.add(obj_size)
        for size_obj in obj_product.shopee_size.all():
            if size_obj.size:
                obj_product.size.add(size_obj.size)
            else:                # 사이즈 정보 중 없는 정보가 있으면 R로 변경
                obj_product.validation = 'R'

    def __update_color(self, obj_product, options):
        for option in options:
            obj_color, is_created = ShopeeColor.objects.get_or_create(
                display_name=self.__get_cleaned_text(option))
            obj_product.shopee_color.add(obj_color)
        for color_obj in obj_product.shopee_color.all():
            if color_obj.color:
                obj_product.color.add(color_obj.color)
            else:                # 사이즈 정보 중 없는 정보가 있으면 R로 변경
                obj_product.validation = 'R'

    def __update_product_option(self, obj_product, option_list, color_index, size_index, has_extra_options):
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
                    product=obj_product, shopee_item_id=option['modelid'])
                if is_created:
                    # 옵션 생성 후에는 기본 옵션 정보 선택이 필요.
                    if color_index is None and size_index is None:
                        if len(option_list) == 1:
                            if option['name'] == '':
                                obj_option.name = 'default option(ONE SIZE)'
                            else:
                                obj_option.name = option['name']
                            obj_option.extra_option = None
                            obj_option.size = free_size_obj
                            obj_option.color = u_color_obj
                        else:
                            not_valid_information = True
                            break
                    else:
                        obj_option.name = option['name']
                        splited_list = option['name'].lower().split(',')
                        if color_index != None:
                            obj_color, is_created = ShopeeColor.objects.get_or_create(
                                display_name=self.__get_cleaned_text(splited_list[color_index]))
                            if obj_color.color:
                                obj_option.color = obj_color.color
                            else:
                                obj_product.validation = 'R'
                                not_valid_information = True
                                break
                        else:
                            obj_option.color = u_color_obj

                        if size_index != None:
                            obj_size, is_created = ShopeeSize.objects.get_or_create(
                                display_name=self.__get_cleaned_text(splited_list[size_index]))
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
                obj_option.save()

            if has_extra_options or not_valid_information:
                for option in option_list:
                    obj_option, is_created = ProductOption.objects.get_or_create(
                        product=obj_product, shopee_item_id=option['modelid'])
                    if is_created:
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
                    obj_option.save()

    def __update_price(self, obj_product, data):
        if (data['show_discount'] == 0) == obj_product.is_discount:
            print('p', end='')
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
            obj_product.shipping_price = 25000
        obj_product.save()

    def get_or_create_product(self, store_obj, itemid, view_count=None):
        shopid = store_obj.shopee_numeric_id
        # 0. 상품 생성 및 호출
        obj_product, is_created = Product.objects.get_or_create(
            shopee_item_id=itemid, store=store_obj)
        # print('https://dabivn.com/admin/product/product/'+str(obj_product.pk))
        print('.', end='')
        # 0. 상품 json load
        data = self.__request_url_item(shopid, itemid).json()['item']
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
                print('new product created')
                obj_product.validation = 'V'
                self.__update_category(obj_product, data['categories'])
                obj_product.product_link = store_obj.shopee_url + '/' + str(itemid)
                obj_product.created_at = datetime.datetime.fromtimestamp(
                    int(data['ctime']), pytz.UTC)
                obj_product.product_source = 'SHOPEE'
                obj_product.name = data['name']
                obj_product.description = data['description']
                # image
                obj_product.product_thumbnail_image = 'https://cf.shopee.vn/file/' + \
                    data['image'] + '_tn'
                for product_image in data['images']:
                    obj_image, image_is_created = ProductImage.objects.get_or_create(
                        source='https://cf.shopee.vn/file/' + product_image,
                        source_thumb='https://cf.shopee.vn/file/' + product_image+'_tn',
                        product=obj_product,
                        post_image_type='P')

            # 2. 상품 사이즈 / 컬러 정보 업데이트
                if (data['size_chart'] != None):
                    obj_product.size_chart = 'https://cf.shopee.vn/file/' + data['size_chart']
                for i, variation in enumerate(data['tier_variations']):
                    variation_name = variation['name'].replace(':', '').lower().strip()
                    if variation_name == 'size' or variation_name == 'kích cỡ' or variation_name == 'kích thước':
                        self.__update_size(obj_product, variation['options'])
                        size_index = i
                    elif 'màu' in variation_name or 'color' in variation_name:
                        self.__update_color(obj_product, variation['options'])
                        color_index = i
                    else:
                        self.__update_extra_options(obj_product, variation)
                        has_extra_options = True
                if obj_product.size.count() == 0:
                    self.__update_size(obj_product, ['free'])

            # 3. 기존 / 신규 상품 업데이트
            # 3. 가격 및 레이팅 업데이트
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
            obj_product.save()

            # 4. 옵션 생성 및 업데이트
            self.__update_product_option(obj_product, data['models'], color_index, size_index, has_extra_options)

            # 5. 생성 후 최종 검증
            if is_created:
                if obj_product.validation == 'V' and obj_product.stock_available:
                    obj_product.is_active = True
                    obj_product.save()
                if obj_product.validation == 'R':
                    obj_product.is_active = False
                    obj_product.save()
        return obj_product

    def search_store(self, store_obj):
        i = 0
        pk = 0
        list_length = 100
        store_id = store_obj.insta_id
        while list_length == 100:
            response = self.__request_url(
                store_id=store_obj.shopee_numeric_id, limit=list_length, newest=i*100)
            product_list = response.json()['items']
            for j, product in enumerate(product_list):
                # print("{} - #{} product".format(store_id, i*list_length+j+1))
                product_obj = self.get_or_create_product(
                    store_obj, product['itemid'], product['view_count'])
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
        return pk


def update_shopee():
    obj = ShopeeScraper()
    store_list = Store.objects.filter(
        Q(store_type='IS') |
        Q(store_type='IFSH') |
        Q(store_type='IF(P)SH') |
        Q(store_type='IS(P)')
    ).filter(is_active=True)
    file_path = './shopee_result.txt'
    with open(file_path, "w") as f:
        for i, store_obj in enumerate(store_list):
            print("\n  #" + str(i) + ' update ' + str(store_obj))
            updated = obj.search_store(store_obj)
            result_text = store_obj.insta_id + 'total : ' + str(updated) + '\n'
            f.writelines(result_text)
    slack_upload_file(file_path)
    os.remove(file_path)


def validate_shopee():
    obj = ShopeeScraper()
    store_list = Store.objects.filter(store_type='IS').filter(is_active=True)
    for i, store_obj in enumerate(store_list):
        print("\n  #" + str(i) + ' update ' + str(store_obj))
        product_list = Product.objects.filter(is_active=True, store=store_obj, product_source='SHOPEE')
        for product_obj in product_list:
            obj.get_or_create_product(store_obj, product_obj.shopee_item_id)


def multi(product_obj):
    obj = ShopeeScraper()
    store = product_obj.store
    if store:
        print('update ' + 'https://dabivn.com/admin/product/product/' + str(product_obj.pk))
        obj.get_or_create_product(store, product_obj.shopee_item_id)


if __name__ == '__main__':
    # pool = mp.Pool(processes=64)
    # store_obj = Store.objects.get(insta_id='nobsilver')
    # product_list = Product.objects.filter(store=store_obj, product_source='SHOPEE',)
    # #   is_active=False, validation='R', stock_available=True)
    # print('setup multiprocessing')
    # pool.map(multi, product_list)
    # pool.close()

    # for po in product_list:
    # #     multi(po)

    store_obj = Store.objects.get(insta_id='milinaa.clothing')
    obj = ShopeeScraper()
    obj.search_store(store_obj)
    # validate_shopee()
