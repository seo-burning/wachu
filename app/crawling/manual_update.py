from ic_update import preview_image_update
import os_setup
from store.models import Store, StorePost, StoreRanking, PostImage
from product.models import Product, ProductOption, ProductSize
import multiprocessing as mp


def make_deactive_product_by_store(store):
    product_list = Product.objects.filter(store=store)
    for product_obj in product_list:
        product_obj.is_active = False
        product_obj.save()


def make_product_options_from_product(product):
    product_size_list = product.size.all()
    product_color_list = product.color.all()
    original_price = product.original_price
    discount_price = product.discount_price
    discount_rate = product.discount_rate
    name = product.name
    is_free_ship = product.is_free_ship
    if is_free_ship:
        shipping_price = 0
    else:
        shipping_price = 25000
    is_active = product.is_active
    stock = 999
    print('////', len(product_size_list), len(product_color_list))
    if (len(product_size_list) == 0) & (len(product_color_list) == 0):
        print('create free option')
        product_free_size = ProductSize.objects.get(name='free')
        product_option, is_created = ProductOption.objects.get_or_create(
            product=product, size=product_free_size, color=None
        )
        product_option.original_price = original_price
        product_option.discount_price = discount_price
        product_option.discount_rate = discount_rate
        product_option.is_free_ship = is_free_ship
        product_option.shipping_price = shipping_price
        product_option.name = name
        product_option.is_active = is_active
        product_option.stock = stock
        product_option.save()
    if (len(product_size_list) > 0) & (len(product_color_list) == 0):
        for product_size in product_size_list:
            product_option, is_created = ProductOption.objects.get_or_create(
                product=product, size=product_size, color=None
            )
            product_option.original_price = original_price
            product_option.discount_price = discount_price
            product_option.discount_rate = discount_rate
            product_option.is_free_ship = is_free_ship
            product_option.shipping_price = shipping_price
            product_option.name = name
            product_option.is_active = is_active
            product_option.stock = stock
            product_option.save()
    elif(len(product_size_list) == 0) & (len(product_color_list) > 0):
        for product_color in product_color_list:
            product_option, is_created = ProductOption.objects.get_or_create(
                product=product, color=product_color, size=None
            )
            product_option.original_price = original_price
            product_option.discount_price = discount_price
            product_option.discount_rate = discount_rate
            product_option.is_free_ship = is_free_ship
            product_option.shipping_price = shipping_price
            product_option.name = name
            product_option.is_active = is_active
            product_option.stock = stock
            product_option.save()
    elif(len(product_size_list) > 0) & (len(product_color_list) > 0):
        for product_size in product_size_list:
            for product_color in product_color_list:
                product_option, is_created = ProductOption.objects.get_or_create(
                    product=product, color=product_color, size=product_size
                )
                product_option.original_price = original_price
                product_option.discount_price = discount_price
                product_option.discount_rate = discount_rate
                product_option.is_free_ship = is_free_ship
                product_option.shipping_price = shipping_price
                product_option.name = name
                product_option.is_active = is_active
                product_option.stock = stock
                product_option.save()
    else:
        print('no options')


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
    pool = mp.Pool(processes=32)
    store_list = Store.objects.filter(is_active=True)
    pool.map(_update_product_category_to_store_category, store_list)
    pool.close()


# daily task
def preview_image_update():
    store_list = Store.objects.filter(is_active=True)
    for store_obj in store_list:
        product_list = Product.objects.filter(store=store_obj, is_active=True).order_by('-created_at')
        store_obj.recent_post_1 = product_list[0].product_thumbnail_image
        store_obj.recent_post_2 = product_list[1].product_thumbnail_image
        store_obj.recent_post_3 = product_list[2].product_thumbnail_image
        store_obj.save()


if __name__ == '__main__':
    product_list = Product.objects.all()
    pool = mp.Pool(processes=64)
    product_list = Product.objects.all()
    pool.map(make_product_options_from_product, product_list)
    pool.close()
