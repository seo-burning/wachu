import multiprocessing as mp
from functools import partial

import os_setup
from product.models import Product, ShopeeRating, ProductImage, ShopeeCategory,\
    ProductSize, ProductColor, ProductExtraOption, \
    ProductOption, ShopeeColor, ShopeeSize, ProductSubCategory, ProductCategory,\
    ProductStyle
from store.models import Store, StorePost, Primary_Style, Age, Category


def update_color(obj_product, options):
    obj_product.color.clear()
    obj_product.shopee_color.clear()
    # print(len(options))
    print(options)
    for option in options:
        option_string = option['display_name'].lower().strip()
        print(option_string)
        obj_color, is_created = ShopeeColor.objects.get_or_create(
            display_name=option_string)
        obj_product.shopee_color.add(obj_color)
        for color_obj in obj_product.shopee_color.all():
            if color_obj.color:
                # print("exist : {} => {}".format(color_obj.display_name, color_obj.color))
                obj_product.color.add(color_obj.color)
            else:
                obj_product.is_active = False
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
            obj_product.is_active = False

    obj_product.save()


def update_product_option(obj_product, option_list):
    for option in option_list:
        print(option['name'], 'created', option)
        obj_option, is_created = ProductOption.objects.get_or_create(
            product=obj_product, name=option['name'])
        obj_option.is_active = option['is_active']
        obj_option.name = option['name']
        obj_option.original_price = option['original_price']
        obj_option.discount_price = option['discount_price']
        obj_option.currency = option['currency']
        obj_option.stock = option['stock']
        if ('size' in option) and (option['size']):
            obj_size = ShopeeSize.objects.get(
                display_name=option['size']['display_name'])
            obj_option.size = obj_size.size
        if ('color' in option) and (option['color']):
            obj_color = ShopeeColor.objects.get(display_name=option['color']['display_name'])
            obj_option.color = obj_color.color
        obj_option.save()
    if len(option_list) == 0:
        print(obj_product.pk, 'no option')
        obj_size = ProductSize.objects.get(
            name='free')
        obj_product.size.add(obj_size)
        print(option['name'], 'created', option)
        obj.product.save()
        obj_option, is_created = ProductOption.objects.get_or_create(
            product=obj_product, name='free')
        obj_option.is_active = True
        obj_option.original_price = obj_product.original_price
        obj_option.discount_price = obj_product.discount_price
        obj_option.currency = obj_product.currency
        obj_option.stock = obj_product.stock
        obj_option.size = obj_size
        obj_option.save()


def update_product_image(obj_product, product_image_list):
    for option in product_image_list:
        try:
            obj_image, is_created = ProductImage.objects.get_or_create(
                product=obj_product,
                source=option['source'],
                source_thumb=option['source'],
                post_image_type=option['post_image_type']
            )
        except:
            pass


def update_sub_category(obj_product, subcategory):
    shopee_category, is_created = ShopeeCategory.objects.get_or_create(display_name=subcategory)
    print(shopee_category.sub_category)
    if shopee_category.sub_category:
        obj_product.shopee_category.add(shopee_category)
        obj_product.sub_category = shopee_category.sub_category
        obj_product.category = shopee_category.category
        obj_product.is_active = True
    else:
        obj_product.shopee_category.add(shopee_category)
        obj_product.is_active = False
    obj_product.save()


def update_style(obj_product, style):
    style_obj = ProductStyle.objects.get(name=style)
    obj_product.style = style_obj
    obj_product.save()


def update_product_object(product_source):
    if ('store' in product_source):
        store_obj = Store.objects.get(pk=product_source['store'])
    elif ('store_name' in product_source):
        store_name = product_source['store_name']
        store_obj = Store.objects.get(insta_id=store_name)
        print(store_name)
    product_obj, is_created = Product.objects.get_or_create(
        name=product_source['name'],
        product_link=product_source['product_link'],
        store=store_obj
    )

    product_obj.is_discount = product_source['is_discount']
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
    product_obj.save()

    if is_created:
        print('this this this')
        product_obj.current_review_rating = product_source['current_review_rating']
        update_product_image(product_obj, product_source['product_image_list'])
        # 아래의 항목들은 최초 생성 후 수동으로 재분류를 하는 경우도 있으니 업데이트하지 않는다.
        if 'subcategory' in product_source:
            update_sub_category(product_obj, product_source['subcategory'])
        product_obj.is_active = product_source['is_active']
        if 'style' in product_source:
            update_style(product_obj, product_source['style'])
        if store_obj.is_active == False:
            product_obj.is_active = False

    update_color(product_obj, product_source['shopee_color'])
    update_size(product_obj, product_source['shopee_size'])
    update_product_option(product_obj, product_source['productOption'])

    product_obj.save()


def dict_to_product_model(product_list):
    print(len(product_list))
    pool = mp.Pool(processes=64)
    print('setup multiprocessing')
    pool.map(update_product_object, product_list)
    pool.close()
    # for product_obj in product_list:
    #     update_product_object(product_obj)


#  {'insta_id': 'dam',
#   'store_type': 'DS',
#   'profile_image': 'https://static.dosi-in.com/images/logos/20/logo.png',
#   'name': 'ĐẬM',
#   'homepage_url': 'https://dosi-in.com/dam/',
#   'primary_style': 'street'}

def update_store_object(store_dic):
    store_obj, is_created = Store.objects.get_or_create(
        insta_id=store_dic['insta_id'], store_type=store_dic['store_type'])
    store_obj.profile_image = store_dic['profile_image']
    store_obj.name = store_dic['name']
    store_obj.is_active = False
    store_obj.homepage_url = store_dic['homepage_url']
    primary_style = Primary_Style.objects.get(name=store_dic['primary_style'])
    age = Age.objects.get(name='10s, 20s')
    category = Category.objects.get(name='cloth_all')
    store_obj.primary_style = primary_style
    store_obj.age = age
    store_obj.category.add(category)
    store_obj.save()


def dict_to_store_model(store_dic_list):
    for store_dic in store_dic_list:
        update_store_object(store_dic)


sub_cat = [{'dosiin': 'sleeveless',
            'subcategory': 'offshoulder_sleeveless'},
           {'dosiin': 'short-sleeve',
            'subcategory': 'tshirts'},
           {'dosiin': 'long-sleeve',
            'subcategory': 'sweatshirts'},
           {'dosiin': 'long-sleeve-vi',
            'subcategory': 'sweater'},
           {'dosiin': 'hoodie-hood-zipup',
            'subcategory': 'hoodie'},
           {'dosiin': 'shirts-blouses',
            'subcategory': 'shirts'},
           #                        {'dosiin':'one-piece',
           #                         'subcategory':'offshoulder_sleeveless'},
           {'dosiin': 'pike-polo',
            'subcategory': 'polo_shirts'},
           {'dosiin': 'ao-croptop',
            'subcategory': 'croptop'},
           {'dosiin': 'ao-thun-basic',
            'subcategory': 'tshirts'}]


def temp():
    for ss in sub_cat:
        print(ss)
        obj, is_created = ShopeeCategory.objects.get_or_create(display_name=ss['dosiin'], catid=1991)
        subcategory_obj = ProductSubCategory.objects.get(name=ss['subcategory'])
        obj.sub_category = subcategory_obj
        obj.category = subcategory_obj.category
        obj.no_sub = True
        obj.is_default_subcat = True
        obj.is_valid = True
        obj.save()
