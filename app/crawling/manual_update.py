import requests
import os_setup
from store.models import Store, StorePost, StoreRanking, PostImage
from product.models import Product, ProductOption, ProductSize
import multiprocessing as mp


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
    queryset = Store.objects.all()[150:]
    for obj in queryset:
        print(obj)
        if obj.insta_url is None:
            insta_is_valid = 'None'
        elif requests.get(obj.insta_url).status_code == 200:
            insta_is_valid = 'True'
        else:
            insta_is_valid = 'False'

        if obj.facebook_url is None:
            facebook_is_valid = 'None'
        elif requests.get(obj.facebook_url).status_code == 200:
            facebook_is_valid = 'True'
        else:
            facebook_is_valid = 'False'

        if obj.homepage_url is None:
            homepage_is_valid = 'None'
        else:
            try:
                if requests.get(obj.homepage_url).status_code == 200:
                    homepage_is_valid = 'True'
                else:
                    homepage_is_valid = 'False'
            except:
                homepage_is_valid = 'False'

        if obj.shopee_url is None:
            shopee_is_valid = 'None'
        elif requests.get(obj.shopee_url).status_code == 200:
            shopee_is_valid = 'True'
        else:
            shopee_is_valid = 'False'
        validation_string = insta_is_valid + '/'+facebook_is_valid+'/'+homepage_is_valid+'/'+shopee_is_valid
        obj.validation_string = validation_string
        obj.save()


if __name__ == '__main__':
    update_store_validation()
