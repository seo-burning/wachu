import os_setup
from product.models import Product
import requests
from homepage.fivetheway import get_5theway
from homepage.dottie import get_dottie
from dosiin.dosiin_crawling import get_dosiin
from homepage.inventory_version import get_olv, get_clothesbar, get_nowsaigon, get_hades, get_dirtycoins,  \
    get_degrey, get_libeworkshop, get_swe, get_blvck, get_tsun, get_tatichubeyoung, get_edini,\
    get_heyyoustudio, get_errorist, get_fusionism, get_shebyshj, get_cecicela, get_lepoulet, get_colin, get_devons
from dict_to_db import dict_to_product_model, dict_to_store_model
from helper.request_helper import get_user_agents
from utils.slack import slack_notify
from store.models import Store

def update_homepage():
    # # fivetheway_result = get_5theway()
    # dict_to_store_model(dosiin_brand)
    # dosiin_result = get_dosiin()
    # dict_to_product_model(dosiin_result)
    home_page_list = [
        get_devons,
        get_olv, get_tsun,
        get_lepoulet,
        get_clothesbar, get_nowsaigon, get_hades,
        get_degrey,
        get_libeworkshop, get_swe, get_blvck, get_tatichubeyoung,
        get_heyyoustudio, get_errorist, get_fusionism, get_shebyshj, get_cecicela,
        get_colin,
        get_dirtycoins,
    ]

    for i, home_page_obj in enumerate(home_page_list):
        try:
            product_list = home_page_obj()
            dict_to_product_model(product_list)
        except:
            slack_notify('error occured homepage crawling ', str(i))


def validate_homepage(store=None):
    if store:
        product_list = Product.objects.filter(store=store)
    else:
        product_list = Product.objects.filter(product_source='HOMEPAGE', is_active=True)
    try:
        for obj_product in product_list:
            print('.', end='')
            response = requests.get(obj_product.product_link,
                                    headers={'User-Agent': get_user_agents(),
                                             'X-Requested-With': 'XMLHttpRequest',
                                             },)
            if response.status_code == 404:
                print('d', end='')
                obj_product.is_active = False
                obj_product.validation = 'D'
                obj_product.name = '[DELETED FROM SOURCE PAGE]' + obj_product.name
                obj_product.save()
    except:
        slack_notify('error occured homepage validating ')


if __name__ == '__main__':
    store = Store.objects.get(insta_id='dirtycoins.vn')
    # validate_homepage()
    update_homepage()
    validate_homepage(store)
    pass
