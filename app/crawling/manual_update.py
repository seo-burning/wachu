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


if __name__ == '__main__':
    update_product_category_to_store_category()
