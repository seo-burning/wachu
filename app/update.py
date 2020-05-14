from product.models import Product, ShopeeRating, ProductImage, ShopeeCategory, ProductSize, ProductColor, ProductExtraOption, ProductOption, ShopeeColor, ShopeeSize
from store.models import Store, StorePost, Primary_Style, Secondary_Style, Age, Category
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


if __name__ == '__main__':
    print('start scrapying')

    product_list = Product.objects.filter(product_image_type='V')
