

import requests
import json
import sys
import os
import django
import time
import datetime
import pytz
import csv
from random import choice
from django.db.models import Q

PROJECT_ROOT = os.getcwd()
sys.path.append(os.path.dirname(PROJECT_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.prod")
django.setup()
from store.models import Store, StorePost, Primary_Style, Secondary_Style, Age, Category
from product.models import Product, ShopeeRating, ProductImage, ShopeeCategory, ProductSize, ProductColor, ProductExtraOption, ProductOption, ShopeeColor, ShopeeSize

if __name__ == '__main__':
    print('start scrapying')

    product_list = Product.objects.filter(product_image_type='V')
    for i, store_obj in enumerate(Store.objects.filter(is_active=True)):
        product_list = Product.objects.filter(store=store_obj, is_active=True)
        if len(product_list) < 3:
            store_obj.is_active = False
            store_obj.save()
            continue
        pic_1 = product_list[0].product_thumbnail_image
        pic_2 = product_list[1].product_thumbnail_image
        pic_3 = product_list[2].product_thumbnail_image
        store_obj.recent_post_1 = pic_1
        store_obj.recent_post_2 = pic_2
        store_obj.recent_post_3 = pic_3
        if(pic_1 == None):
            print(store_obj.insta_id)
        if(pic_2 == None):
            print(store_obj.insta_id)
        if(pic_3 == None):
            print(store_obj.insta_id)
        store_obj.save()
