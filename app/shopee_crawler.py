import requests
import json
import sys
import os
import django
import time
import datetime
import pytz
from random import choice

PROJECT_ROOT = os.getcwd()
sys.path.append(os.path.dirname(PROJECT_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.prod")
django.setup()

from product.models import Product,ShopeeRating,ProductImage,ShopeeCategory,ProductSize,ProductColor
from store.models import Store

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

data = {
'images': [
    '79b47b034140ca5ffc6ccc9552ada5c4',
    '4f54e59904ea3e11f9db45af988b23f4',
    '505158c2f9722e2af4101dd25f8b2e99',
    '94368e51a3eb5689ac04e827df6ad137',
    '7cb1ac353bac4b35d0e0a4143f217c85',
    'd2b730d3c9ea180eaf38a393f4f28866',
    '8426b8e0ae8b54fcaec11fb8bcd56913',
    'f0278cb6033d94b3dd33011a937850b9',
    '640c046ea4175f9673da8fa852496539'
],
'itemid': 2621336840,
'price_max_before_discount': -1,
'price_max': 40000000000,
'price_before_discount': 0,
'show_free_shipping': False,
'categories': [
    {
    'display_name': 'Thời Trang Nam',
    'catid': 78,
    'image': None,
    'no_sub': False,
    'is_default_subcat': False,
    'block_buyer_platform': None
    },
    {
    'display_name': 'Áo thun',
    'catid': 2827,
    'image': None,
    'no_sub': False,
    'is_default_subcat': False,
    'block_buyer_platform': None
    },
    {
    'display_name': 'Áo ngắn tay không cổ',
    'catid': 8947,
    'image': None,
    'no_sub': True,
    'is_default_subcat': False,
    'block_buyer_platform': None
    }
],
'catid': 78,
'ctime': 1565163369,
'name': 'Áo Hologram',
'size_chart': None,
'historical_sold': 187,
'sold': 20,
'item_rating': {
    'rating_star': 4.989796,
    'rating_count': [
    98,
    0,
    0,
    0,
    1,
    97
    ],
    'rcount_with_image': 25,
    'rcount_with_context': 34
},
'show_official_shop_label_in_title': False,
'discount': None,
'reason': '',
'label_ids': [
    1000064,
    1000269,
    1000268,
    1000138,
    1000043,
    1000044,
    1000205,
    1000207,
    1000112,
    1000049,
    1000051,
    1000277,
    1000279,
    1000315,
    1000062,
    1000255
],
'has_group_buy_stock': False,
'deep_discount': None,
'attributes': [
    {
    'is_pending_qc': False,
    'idx': 0,
    'value': 'No Brand',
    'id': 830,
    'is_timestamp': False,
    'name': 'Thương hiệu'
    },
    {
    'is_pending_qc': True,
    'idx': 1,
    'value': 'Cotton',
    'id': 19352,
    'is_timestamp': False,
    'name': 'Chất liệu'
    },
    {
    'is_pending_qc': True,
    'idx': 2,
    'value': '',
    'id': 22359,
    'is_timestamp': False,
    'name': 'Xuất Xứ'
    }
],
'badge_icon_type': 0,
'liked': False,
'cmt_count': 98,
'image': '79b47b034140ca5ffc6ccc9552ada5c4',
'is_cc_installment_payment_eligible': False,
'shopid': 77177153,
'normal_stock': 11,
'video_info_list': [
    
],
'installment_plans': None,
'view_count': None,
'current_promotion_has_reserve_stock': False,
'liked_count': 358,
'show_official_shop_label': False,
'price_min_before_discount': -1,
'show_discount': 0,
'preview_info': None,
'flag': 0,
'current_promotion_reserved_stock': 0,
'wholesale_tier_list': [
    
],
'group_buy_info': None,
'shopee_verified': False,
'hidden_price_display': None,
'transparent_background_image': '',
'welcome_package_info': None,
'coin_info': {
    'spend_cash_unit': 100000,
    'coin_earn_items': [
    
    ]
},
'is_adult': None,
'currency': 'VND',
'raw_discount': 0,
'is_category_failed': False,
'price_min': 40000000000,
'can_use_bundle_deal': False,
'cb_option': 0,
'brand': 'No Brand',
'stock': 11,
'status': 1,
'bundle_deal_id': 0,
'is_group_buy_item': None,
'description': 'Hologram Tee\nSize: S / M / L/ XL.\n100% cotton.\nĐen,Trắng\nDesign by Dirtycoins Studio.\n......................',
'flash_sale': None,
'models': [
    {
    'itemid': 2621336840,
    'status': 1,
    'current_promotion_reserved_stock': 0,
    'name': 'Trắng,S',
    'promotionid': 0,
    'price': 40000000000,
    'current_promotion_has_reserve_stock': False,
    'currency': 'VND',
    'normal_stock': 1,
    'extinfo': {
        'seller_promotion_limit': None,
        'has_shopee_promo': None,
        'group_buy_info': None,
        'holiday_mode_old_stock': None,
        'tier_index': [
        0,
        0
        ],
        'seller_promotion_refresh_time': 0
    },
    'price_before_discount': 0,
    'modelid': 5982030974,
    'sold': 18,
    'stock': 1
    },
    {
    'itemid': 2621336840,
    'status': 1,
    'current_promotion_reserved_stock': 0,
    'name': 'Trắng,M',
    'promotionid': 0,
    'price': 40000000000,
    'current_promotion_has_reserve_stock': False,
    'currency': 'VND',
    'normal_stock': 1,
    'extinfo': {
        'seller_promotion_limit': None,
        'has_shopee_promo': None,
        'group_buy_info': None,
        'holiday_mode_old_stock': None,
        'tier_index': [
        0,
        1
        ],
        'seller_promotion_refresh_time': 0
    },
    'price_before_discount': 0,
    'modelid': 5982030975,
    'sold': 26,
    'stock': 1
    },
    {
    'itemid': 2621336840,
    'status': 1,
    'current_promotion_reserved_stock': 0,
    'name': 'Trắng,L',
    'promotionid': 0,
    'price': 40000000000,
    'current_promotion_has_reserve_stock': False,
    'currency': 'VND',
    'normal_stock': 0,
    'extinfo': {
        'seller_promotion_limit': None,
        'has_shopee_promo': None,
        'group_buy_info': None,
        'holiday_mode_old_stock': None,
        'tier_index': [
        0,
        2
        ],
        'seller_promotion_refresh_time': 0
    },
    'price_before_discount': 0,
    'modelid': 5982030976,
    'sold': 24,
    'stock': 0
    },
    {
    'itemid': 2621336840,
    'status': 1,
    'current_promotion_reserved_stock': 0,
    'name': 'Trắng,XL',
    'promotionid': 0,
    'price': 40000000000,
    'current_promotion_has_reserve_stock': False,
    'currency': 'VND',
    'normal_stock': 1,
    'extinfo': {
        'seller_promotion_limit': None,
        'has_shopee_promo': None,
        'group_buy_info': None,
        'holiday_mode_old_stock': None,
        'tier_index': [
        0,
        3
        ],
        'seller_promotion_refresh_time': 0
    },
    'price_before_discount': 0,
    'modelid': 5982030977,
    'sold': 12,
    'stock': 1
    },
    {
    'itemid': 2621336840,
    'status': 1,
    'current_promotion_reserved_stock': 0,
    'name': 'Đen,S',
    'promotionid': 0,
    'price': 40000000000,
    'current_promotion_has_reserve_stock': False,
    'currency': 'VND',
    'normal_stock': 4,
    'extinfo': {
        'seller_promotion_limit': None,
        'has_shopee_promo': None,
        'group_buy_info': None,
        'holiday_mode_old_stock': None,
        'tier_index': [
        1,
        0
        ],
        'seller_promotion_refresh_time': 0
    },
    'price_before_discount': 0,
    'modelid': 5982030978,
    'sold': 24,
    'stock': 4
    },
    {
    'itemid': 2621336840,
    'status': 1,
    'current_promotion_reserved_stock': 0,
    'name': 'Đen,M',
    'promotionid': 0,
    'price': 40000000000,
    'current_promotion_has_reserve_stock': False,
    'currency': 'VND',
    'normal_stock': 2,
    'extinfo': {
        'seller_promotion_limit': None,
        'has_shopee_promo': None,
        'group_buy_info': None,
        'holiday_mode_old_stock': None,
        'tier_index': [
        1,
        1
        ],
        'seller_promotion_refresh_time': 0
    },
    'price_before_discount': 0,
    'modelid': 5982030979,
    'sold': 24,
    'stock': 2
    },
    {
    'itemid': 2621336840,
    'status': 1,
    'current_promotion_reserved_stock': 0,
    'name': 'Đen,L',
    'promotionid': 0,
    'price': 40000000000,
    'current_promotion_has_reserve_stock': False,
    'currency': 'VND',
    'normal_stock': 0,
    'extinfo': {
        'seller_promotion_limit': None,
        'has_shopee_promo': None,
        'group_buy_info': None,
        'holiday_mode_old_stock': None,
        'tier_index': [
        1,
        2
        ],
        'seller_promotion_refresh_time': 0
    },
    'price_before_discount': 0,
    'modelid': 5982030980,
    'sold': 33,
    'stock': 0
    },
    {
    'itemid': 2621336840,
    'status': 1,
    'current_promotion_reserved_stock': 0,
    'name': 'Đen,XL',
    'promotionid': 0,
    'price': 40000000000,
    'current_promotion_has_reserve_stock': False,
    'currency': 'VND',
    'normal_stock': 2,
    'extinfo': {
        'seller_promotion_limit': None,
        'has_shopee_promo': None,
        'group_buy_info': None,
        'holiday_mode_old_stock': None,
        'tier_index': [
        1,
        3
        ],
        'seller_promotion_refresh_time': 0
    },
    'price_before_discount': 0,
    'modelid': 5982030981,
    'sold': 27,
    'stock': 2
    }
],
'price': 40000000000,
'shop_location': 'TP. Hồ Chí Minh',
'tier_variations': [
    {
    'images': None,
    'properties': None,
    'type': 0,
    'name': 'Màu',
    'options': [
        'Trắng',
        'Đen'
    ]
    },
    {
    'images': None,
    'properties': None,
    'type': 0,
    'name': 'Size',
    'options': [
        'S',
        'M',
        'L',
        'XL'
    ]
    }
],
'makeups': None,
'welcome_package_type': 0,
'show_official_shop_label_in_normal_position': None,
'item_type': 0
}

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

    def __request_url(self, url):
        try:
            response = requests.get('https://shopee.vn/api/v2/search_items/?by=pop&limit=30&match_id='+url+'&newest=0&order=desc&page_type=shop&shop_categoryids=&version=2', headers={'User-Agent': self.__random_agent(),         
                                                    'X-Requested-With': 'XMLHttpRequest',
                                                    'Referer':'https://shopee.vn/shop/'+url+'/search?shopCollection=',
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

    def __request_url_item(self, store_id,item_id):
        try:
            response = requests.get("https://shopee.vn/api/v2/item/get?itemid={item_id}&shopid={store_id}".format(item_id=item_id,store_id=store_id), headers={'User-Agent': self.__random_agent(),         
                                                    'X-Requested-With': 'XMLHttpRequest',
                                                    'Referer':'https://shopee.vn/shop/'+str(store_id)+'/search?shopCollection=',
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
            print(category)
            obj_cat, is_created = ShopeeCategory.objects.get_or_create(catid=int(category['catid']),
            display_name=category['display_name'])
            print(obj_cat, is_created)
            obj_product.shopee_category.add(obj_cat)
        obj_product.save()


    def __update_size(self, obj_product, options):
        for option in options:
            obj_size, is_created = ProductSize.objects.get_or_create(name=option)
            obj_product.size.add(obj_size)
        obj_product.save()

    def __update_color(self, obj_product, options):
        for option in options:
            obj_color, is_created = ProductColor.objects.get_or_create(display_name=option)
            if is_created:
                print('created')
                obj_color.name = option
                obj_color.save()
            obj_product.color.add(obj_color)
        obj_product.save()

    def __update_rating(self, obj_product, data):
        obj_rating, is_created = ShopeeRating.objects.get_or_create(product=obj_product)
        if data['liked_count']:
            obj_rating.shopee_liked_count = data['liked_count']
        if data['historical_sold']:
            obj_rating.shopee_sold_count = data['historical_sold']
        if data['view_count']:
            obj_rating.shopee_view_count = data['view_count']
        if data['item_rating']['rating_star']:
            obj_rating.shopee_rating_star = data['item_rating']['rating_star']
        if data['cmt_count']:
            obj_rating.shopee_review_count = data['cmt_count']
        obj_rating.save()


    def __update_price(self, obj_product, data):
        print(data['price'],data['raw_discount'],data['price_min_before_discount'])
        if data['show_discount'] == 0:
            obj_product.original_price = data['price'] / 10000
            obj_product.discount_rate = data['raw_discount']
            obj_product.currency = data['currency']
        else:
            obj_product.original_price = data['price_min_before_discount'] / 10000
            obj_product.discount_price = data['price'] / 10000
            obj_product.discount_rate = data['raw_discount']
            obj_product.currency = data['currency']
        obj_product.save()

    def __get_or_create_product(self, data, store_obj):
        itemid = data['itemid']
        shopid = data['shopid']
        # basic info
        obj_product, is_created = Product.objects.get_or_create(
                shopee_item_id=itemid, store=store_obj)
        data = self.__request_url_item(shopid,itemid).json()['item']
        self.__update_category(obj_product, data['categories'])

        obj_product.is_active = True
        obj_product.created_at= datetime.datetime.fromtimestamp(int(data['ctime']), pytz.UTC)
        if (data['size_chart'] != None):
            obj_product.size_chart = data['size_chart']

        obj_product.product_source = 'SHOPEE'
        obj_product.name = data['name']
        obj_product.description = data['description']
        print(data)

        # image
        obj_product.product_thumbnail_image = data['image']
        print(data['image'])
        for product_image in data['images']:
            obj_image, image_is_created = ProductImage.objects.get_or_create(
                                        source='https://cf.shopee.vn/file/' + product_image,
                                        source_thumb='https://cf.shopee.vn/file/' + product_image+'_tn',
                                        product=obj_product,
                                        post_image_type='P')


        obj_product.is_free_ship = data['show_free_shipping']
        obj_product.stock = data['stock']

        for variation in data['tier_variations']:
            if variation['name'] == 'Size':
                self.__update_size(obj_product, variation['options'])
            elif variation['name'] == 'Màu':
                self.__update_color(obj_product, variation['options'])
            print(variation['name'])
        self.__update_price(obj_product, data)
        self.__update_rating(obj_product, data)
        obj_product.save()
    
    def search_store(self,store_id):
        response = self.__request_url(store_id)
        store_obj = Store.objects.get(pk=7)
        product_list = response.json()['items']
        for product in product_list:
            self.__get_or_create_product(product,store_obj)
            break



if __name__ == '__main__':
    print('start scrapying')
    start_time = time.time()
    obj = ShopeeScraper()
    obj.search_store('77177153')
    # obj_product= Product.objects.all().filter(
    #     shopee_item_id=2621336840)[0]
    

