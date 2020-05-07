import multiprocessing as mp
from functools import partial

import os_setup
from product.models import Product, ShopeeRating, ProductImage, ShopeeCategory, ProductSize, ProductColor, ProductExtraOption, ProductOption, ShopeeColor, ShopeeSize
from store.models import Store, StorePost

# {
#     'is_active': False,
#     'is_discount': True,
#     'current_review_rating': 0,
#     'product_source': 'HOMEPAGE',
#     'product_link': 'https://degrey.vn/products/fire-shirt-fs',
#     'store': 291,
#     'name': 'Fire Shirt - FS',
#     'description': 'Fire Shirt - FS',
#     'product_image_type': 'MP',
#     'product_thumbnail_image': 'http://product.hstatic.net/1000281824/product/6159ad75-666f-4b9a-85ae-4e17f53c70ed_69497d9df1c24ba582541ff256f5fd10_grande.jpeg',
#     'video_source': None,
#     'original_price': '350000',
#     'discount_price': '315000',
#     'discount_rate': '10',
#     'currency': 'VND',
#     'is_free_ship': False,
#     'stock': 9999,
#     'shopee_color': [{'display_name': 'NHỎ'},
#                      {'display_name': 'TRUNG'},
#                      {'display_name': 'LỚN'}],
#     'shopee_size': [],
#     'shopee_category': [],
#     'size_chart': None,
#     'productOption': []
# }


def update_color(obj_product, options):
    obj_product.color.clear()
    obj_product.shopee_color.clear()
    # print(len(options))
    # print(options)
    for option in options:
        option_string = option['display_name'].lower().strip()
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


def update_size(obj_product, options):
    obj_product.size.clear()
    obj_product.shopee_size.clear()
    for option in options:
        option_string = option['display_name'].lower().replace('size', '').replace(' ', '').strip()
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


def update_product_option(obj_product, option_list):
    for option in option_list:
        print(option['name'], 'created')
        obj_option, is_created = ProductOption.objects.get_or_create(
            product=obj_product, name=option['name'])
        obj_option.is_active = option['is_active']
        obj_option.name = option['name']
        obj_option.original_price = option['original_price']
        obj_option.discount_price = option['discount_price']
        obj_option.currency = option['currency']
        obj_option.stock = option['stock']
        obj_option.save()


def update_product_image(obj_product, product_image_list):
    for option in product_image_list:
        obj_image, is_created = ProductImage.objects.get_or_create(
            product=obj_product,
            source=option['source'],
            source_thumb=option['source'],
            post_image_type=option['post_image_type']
        )


def update_product_object(product_source):
    store_obj = Store.objects.get(pk=product_source['store'])
    product_obj, is_created = Product.objects.get_or_create(
        name=product_source['name'],
        product_link=product_source['product_link'],
        store=store_obj
    )
    product_obj.is_active = product_source['is_active']
    product_obj.is_discount = product_source['is_discount']
    product_obj.current_review_rating = product_source['current_review_rating']
    product_obj.product_source = product_source['product_source']
    product_obj.description = product_source['description']
    product_obj.product_thumbnail_image = product_source['product_thumbnail_image']
    product_obj.video_source = product_source['video_source']
    product_obj.original_price = product_source['original_price']
    product_obj.discount_price = product_source['discount_price']
    product_obj.discount_rate = product_source['discount_rate']
    product_obj.currency = product_source['currency']
    product_obj.is_free_ship = product_source['is_free_ship']
    product_obj.product_thumbnail_image = product_source['product_thumbnail_image']
    product_obj.stock = product_source['stock']
    product_obj.size_chart = product_source['size_chart']
    update_color(product_obj, product_source['shopee_color'])
    update_size(product_obj, product_source['shopee_size'])
    update_product_option(product_obj, product_source['productOption'])
    update_product_image(product_obj, product_source['product_image_list'])
    product_obj.save()


def dict_to_product_model(product_list):
    pool = mp.Pool(processes=6)
    print('setup multiprocessing')
    pool.map(update_product_object, product_list)
    pool.close()
