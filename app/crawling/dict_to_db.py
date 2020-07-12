from random import choice
import requests
import multiprocessing as mp
from functools import partial


import os_setup
from product.models import Product, ShopeeRating, ProductImage, ShopeeCategory,\
    ProductSize, ProductColor, ProductExtraOption, \
    ProductOption, ShopeeColor, ShopeeSize, ProductSubCategory, ProductCategory,\
    ProductStyle, ProductPattern
from store.models import Store, StorePost, Primary_Style, Age, Category
from datetime import datetime
from django.utils import timezone
from helper.clean_text import get_cleaned_text, remove_html_tags, get_cleaned_text_from_pattern


def get_default_description(obj_product):
    text = obj_product.name + '\n\n'
    text += 'store : ' + obj_product.store.insta_id
    if obj_product.style:
        text += '\n\nstyle : ' + str(obj_product.style)
    text += '\n\n\n\nsize option : '
    for obj in obj_product.size.all():
        text += str(obj) + ' '
    text += '\n\ncolor option : '
    for obj in obj_product.color.all():
        text += str(obj) + ' '
    text += '\n\n' + obj_product.product_link
    return text


def update_color(obj_product, options):
    # obj_product.color.clear()
    # obj_product.shopee_color.clear()
    for option in options:
        option_string = get_cleaned_text_from_pattern(get_cleaned_text(option['display_name']))
        obj_color, is_created = ShopeeColor.objects.get_or_create(
            display_name=option_string)
        obj_product.shopee_color.add(obj_color)
        for color_obj in obj_product.shopee_color.all():
            if color_obj.color:
                obj_product.color.add(color_obj.color)
            else:
                obj_product.validation = 'R'
                obj_product.is_active = False
    obj_product.save()


def update_size(obj_product, options):
    # obj_product.size.clear()
    # obj_product.shopee_size.clear()
    for option in options:
        option_string = get_cleaned_text(option['display_name'])
        obj_size, is_created = ShopeeSize.objects.get_or_create(
            display_name=option_string)
        obj_product.shopee_size.add(obj_size)
    for size_obj in obj_product.shopee_size.all():
        if size_obj.size:
            obj_product.size.add(size_obj.size)
        else:
            obj_product.validation = 'R'
            obj_product.is_active = False
    obj_product.save()


def update_pattern(obj_product):
    pattern_list = ProductPattern.objects.all()
    for pattern_obj in pattern_list:
        name_string = get_cleaned_text(obj_product.name)
        if get_cleaned_text(pattern_obj.name) in name_string or get_cleaned_text(pattern_obj.display_name) in name_string:
            obj_product.pattern.add(pattern_obj)


def make_default_option(obj_product, free_size_obj, u_color_obj):
    obj_product.size.add(free_size_obj)
    obj_product.save()
    obj_option, is_created = ProductOption.objects.get_or_create(
        product=obj_product, shopee_item_id=0)
    if is_created:
        obj_product.name = 'default option(ONE SIZE)'
        obj_option.size = free_size_obj
        obj_option.color = u_color_obj
    obj_option.is_active = True
    obj_option.original_price = obj_product.original_price
    obj_option.discount_price = obj_product.discount_price
    obj_option.currency = obj_product.currency
    obj_option.stock = obj_product.stock
    obj_option.save()


def update_product_option(obj_product, option_list):
    free_size_obj = ProductSize.objects.get(name='free')
    u_color_obj = ProductColor.objects.get(name='undefined')
    u_size_obj = ProductSize.objects.get(name='undefined')

    if len(option_list) == 0:
        make_default_option(obj_product, free_size_obj, u_color_obj)

    not_valid_information = False
    # print('http://dabivn.com/admin/product/product/'+str(obj_product.pk))
    for option in option_list:
        obj_option, is_created = ProductOption.objects.get_or_create(
            product=obj_product, shopee_item_id=option['shopee_item_id'])
        if is_created:
            obj_option.name = option['name']

            if option['size']:
                obj_size = ShopeeSize.objects.get(
                    display_name=get_cleaned_text(option['size']['display_name']))
                if obj_size.size:
                    obj_option.size = obj_size.size
                else:
                    obj_product.validation = 'R'
                    not_valid_information = True
                    break
            else:
                obj_option.size = u_size_obj

            if option['color']:
                obj_color = ShopeeColor.objects.get(display_name=get_cleaned_text_from_pattern(
                    get_cleaned_text(option['color']['display_name'])))
                if obj_color.color:
                    obj_option.color = obj_color.color
                else:
                    obj_product.validation = 'R'
                    not_valid_information = True
                    break
            else:
                obj_option.color = u_color_obj

            if (option['size'] is None) and (option['color'] is None):
                obj_product.validation = 'R'
                not_valid_information = True
                break

        obj_option.currency = option['currency']
        obj_option.original_price = option['original_price']
        obj_option.discount_price = option['discount_price']
        obj_option.is_active = option['is_active']
        obj_option.stock = option['stock']
        try:
            obj_option.save()
        except:
            not_valid_information = True
            obj_product.validation = 'R'
            break

    if not_valid_information:
        for option in option_list:
            obj_option, is_created = ProductOption.objects.get_or_create(
                product=obj_product, shopee_item_id=option['shopee_item_id'])
            obj_option.name = option['name']
            obj_option.extra_option = option['name']
            obj_option.color = u_color_obj
            obj_option.size = u_size_obj
            obj_option.currency = option['currency']
            obj_option.original_price = option['original_price']
            obj_option.discount_price = option['discount_price']
            obj_option.is_active = option['is_active']
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


def update_sub_category(obj_product, subcategory):
    shopee_category, is_created = ShopeeCategory.objects.get_or_create(
        display_name=subcategory, catid=obj_product.store.pk)
    if shopee_category.sub_category:
        obj_product.shopee_category.add(shopee_category)
        obj_product.sub_category = shopee_category.sub_category
        obj_product.category = shopee_category.category
        obj_product.is_active = True
    else:
        obj_product.shopee_category.add(shopee_category)
        obj_product.validation = 'R'
        obj_product.is_active = False
    obj_product.save()


def update_style(obj_product, style):
    style_obj = ProductStyle.objects.get(name=style)
    obj_product.style = style_obj
    obj_product.save()


def update_obj_product(product_source):
    if ('store' in product_source):
        store_obj = Store.objects.get(pk=product_source['store'])
    elif ('store_name' in product_source):
        store_name = product_source['store_name']
        store_obj = Store.objects.get(insta_id=store_name)
    obj_product, is_created = Product.objects.get_or_create(
        product_link=product_source['product_link'],
        store=store_obj
    )
    print('u', end='')
    if product_source['description'] == None or product_source['description'] == '':
        obj_product.description = get_default_description(obj_product)
    elif len(product_source['description']) < 40:
        description = remove_html_tags(product_source['description']) + '\n'+get_default_description(obj_product)
        obj_product.description = description
    else:
        obj_product.description = remove_html_tags(product_source['description'])
    if is_created:
        obj_product.validation = 'V'
        obj_product.name = product_source['name']
        if (product_source['product_thumbnail_image'] == None) or (product_source['product_thumbnail_image'] == ''):
            obj_product.product_thumbnail_image = "http://dabivn.com"
        else:
            obj_product.product_thumbnail_image = product_source['product_thumbnail_image']
        update_product_image(obj_product, product_source['product_image_list'])
        obj_product.video_source = product_source['video_source']
        if 'created_at' in product_source:
            if product_source['created_at']:
                try:
                    created_at = datetime.strptime(product_source['created_at'], "%Y-%m-%dT%H:%M:%S.%f")
                except:
                    created_at = datetime.strptime(product_source['created_at'], "%Y-%m-%dT%H:%M:%S")
                obj_product.created_at = created_at
        obj_product.current_review_rating = product_source['current_review_rating']
        obj_product.product_source = product_source['product_source']
        obj_product.size_chart = product_source['size_chart']
        obj_product.currency = product_source['currency']

        # 아래의 항목들은 최초 생성 후 수동으로 재분류를 하는 경우도 있으니 업데이트하지 않는다.
        if 'subcategory' in product_source:
            update_sub_category(obj_product, product_source['subcategory'])
        obj_product.is_active = product_source['is_active']
        if 'style' in product_source and product_source['style']:
            update_style(obj_product, product_source['style'])
        update_color(obj_product, product_source['shopee_color'])
        update_size(obj_product, product_source['shopee_size'])
        update_pattern(obj_product)

    # 3. 가격 및 레이팅 업데이트
    obj_product.updated_at = timezone.now()
    obj_product.is_discount = product_source['is_discount']
    obj_product.original_price = product_source['original_price']
    obj_product.discount_price = product_source['discount_price']
    obj_product.discount_rate = product_source['discount_rate']
    obj_product.is_free_ship = product_source['is_free_ship']

    # 3. 재고 및 품절 처리
    obj_product.stock = product_source['stock']
    if product_source['stock'] == 0:
        obj_product.is_active = False
        obj_product.stock_available = False
    else:
        obj_product.stock_available = True

    # 4. 옵션 생성 및 업데이트
    update_product_option(obj_product, product_source['productOption'])
    obj_product.save()

    # 5. 생성 후 최종 검증
    if is_created:
        if obj_product.validation == 'V' and obj_product.stock_available:
            obj_product.is_active = True
            obj_product.save()
        if obj_product.validation == 'R':
            obj_product.is_active = False
            obj_product.save()


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


def validate_homepage():
    product_list = Product.objects.filter(product_source='HOMEPAGE')
    for obj_product in product_list:
        response = requests.get(obj_product.product_link,
                                headers={'User-Agent': choice(_user_agents),
                                         'X-Requested-With': 'XMLHttpRequest',
                                         },)
        if response.status_code == 404:
            obj_product.is_active = False
            obj_product.validation = 'D'
            obj_product.name = '[DELETED FROM SOURCE PAGE]' + obj_product.name
            obj_product.save()


def dict_to_product_model(product_list):
    print('\n')
    for obj_product in product_list:
        update_obj_product(obj_product)

    # pool = mp.Pool(processes=2)
    # pool.map(update_obj_product, product_list)
    # pool.close()
