from ic_update import preview_image_update
import os_setup
from store.models import Store, StorePost, StoreRanking, PostImage
from product.models import Product, ProductOption


def make_active_product_by_store(store):
    product_list = Product.objects.filter(store=store)
    for product_obj in product_list:
        product_obj.is_active = True
        product_obj.save()


def make_product_options_from_product(product):
    product_size_list = product.size.all()
    product_color_list = product.color.all()
    original_price = product.original_price
    discount_price = product.discount_price
    discount_rate = product.discount_rate
    name = product.name
    is_free_ship = True
    shipping_price = 0
    is_active = True
    stock = 999

    print('////', len(product_size_list), len(product_color_list))
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


if __name__ == '__main__':
    product_list = Product.objects.filter(is_active=True, is_free_ship=False)
    print(len(product_list))
    for product_obj in product_list:
        product_option_list = ProductOption.objects.filter(product=product_obj)
        print(product_obj.name)
        for product_option_obj in product_option_list:
            print('saved')
            product_option_obj.shipping_price = 25000
            product_option_obj.save()
    # import multiprocessing as mp
    # pool = mp.Pool(processes=6)
    # pool.map(make_product_options_from_product, product_list)
    # pool.close()
