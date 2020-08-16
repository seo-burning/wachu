

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
import multiprocessing as mp

PROJECT_ROOT = os.getcwd()
sys.path.append(os.path.dirname(PROJECT_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.prod")
django.setup()
from store.models import Store, StorePost, Primary_Style, Secondary_Style, Age, Category
from product.models import Product, ShopeeRating, ProductImage, ShopeeCategory, ProductSize, ProductColor, ProductExtraOption, ProductOption, ShopeeColor, ShopeeSize

def temp(obj):
    if obj.is_free_ship == True:
        obj.shipping_price = 0
        print('.', end='')
    else:
        obj.shipping_price = None
        print('!', end='')
    obj.save()
    
if __name__ == '__main__':
    print('start scrapying')
    pool = mp.Pool(processes=64)
    product_list = ProductOption.objects.all()
    pool.map(temp, product_list)
    pool.close()