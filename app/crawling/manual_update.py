import requests
import os_setup
from store.models import Store, StorePost, StoreRanking, PostImage
from product.models import Product, ProductOption, ProductSize
import multiprocessing as mp
from helper.request_helper import get_user_agents


def make_deactive_product_by_store(store):
    product_list = Product.objects.filter(store=store)
    for product_obj in product_list:
        product_obj.is_active = False
        product_obj.save()


def _update_product_category_to_store_category(store_obj):
    print(store_obj.insta_id)
    product_list = Product.objects.filter(store=store_obj)
    product_category_list = []
    for product_obj in product_list:
        if(product_obj.category):
            if (product_obj.category not in product_category_list):
                product_category_list.append(product_obj.category)
    print(product_category_list)
    for product_category in product_category_list:
        store_obj.product_category.add(product_category)
    store_obj.save()


def update_product_category_to_store_category():
    store_list = Store.objects.filter(is_active=True)
    for store_obj in store_list:
        _update_product_category_to_store_category(store_obj)


# daily task
def preview_image_update():
    store_list = Store.objects.filter(is_active=True)
    for store_obj in store_list:
        product_list = Product.objects.filter(store=store_obj, is_active=True).order_by('-created_at')
        if len(product_list) < 3:
            store_obj.is_active = False
            store_obj.save()
        else:
            store_obj.recent_post_1 = product_list[0].product_thumbnail_image
            store_obj.recent_post_2 = product_list[1].product_thumbnail_image
            store_obj.recent_post_3 = product_list[2].product_thumbnail_image
            store_obj.save()


def update_store_validation():
    obj = Store.objects.get(insta_id='aokaie')
    for obj in queryset:
        # 인스타 200 체크
        if obj.insta_url is None:
            insta_is_valid = 'None'
        elif requests.get(obj.insta_url,
                          headers={'User-Agent': get_user_agents(),
                                   'X-Requested-With': 'XMLHttpRequest',
                                   'Referer': 'https://www.instagram.com'}).status_code == 200:
            insta_is_valid = 'True'
        else:
            insta_is_valid = 'False'

        if obj.facebook_url is None:
            facebook_is_valid = 'None'
        elif requests.get(obj.facebook_url,
                          headers={'User-Agent': get_user_agents(),
                                   'X-Requested-With': 'XMLHttpRequest'}).status_code == 200:
            facebook_is_valid = 'True'
        else:
            facebook_is_valid = 'False'

        if obj.homepage_url is None:
            homepage_is_valid = 'None'
        else:
            try:
                if requests.get(obj.homepage_url,
                                headers={'User-Agent': get_user_agents(),
                                         'X-Requested-With': 'XMLHttpRequest'}).status_code == 200:
                    homepage_is_valid = 'True'
                else:
                    homepage_is_valid = 'False'
            except:
                homepage_is_valid = 'False'

        if obj.shopee_url is None:
            shopee_is_valid = 'None'
        else:
            response_json = requests.get('https://shopee.vn/api/v2/search_items/?by=pop&limit=1&match_id'
                                         '={shopee_numeric_id}&newest=1&order=desc&page_type='
                                         'shop&shop_categoryids=&version=2'.format(
                                             shopee_numeric_id=obj.shopee_numeric_id),
                                         headers={'User-Agent': get_user_agents(),
                                                  'X-Requested-With': 'XMLHttpRequest',
                                                  'Referer': 'https://shopee.vn/shop/{store_id}/'
                                                  'search?shopCollection='.format(store_id=obj.shopee_numeric_id),
                                                  },).json()
            if response_json['total_count'] == 0:
                print('this')
                shopee_is_valid = 'False'
            else:
                shopee_is_valid = 'True'
        validation_string = insta_is_valid + '/'+facebook_is_valid+'/'+homepage_is_valid+'/'+shopee_is_valid
        obj.validation_string = validation_string
        obj.save()


if __name__ == '__main__':
    preview_image_update()
