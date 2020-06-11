from homepage.degrey import get_degrey
from homepage.swe import get_swe
from homepage.fivetheway import get_5theway
from homepage.hades import get_hades
from homepage.dottie import get_dottie
from homepage.dirtycoins import get_dirtycoins
from dosiin.dosiin_crawling import get_dosiin
from dict_to_db import dict_to_product_model, dict_to_store_model, temp

if __name__ == '__main__':
    print('start scrapying')
    # dict_to_store_model(dosiin_brand)
    # dosiin_result = get_dosiin()
    # dict_to_product_model(dosiin_result)
    # degrey_result = get_degrey()
    # dict_to_product_model(degrey_result)
    # swe_result = get_swe()
    # dict_to_product_model(swe_result)
    # # fivetheway_result = get_5theway()
    # hades_result = get_hades()
    # dict_to_product_model(hades_result)
    # dottie_result = get_dottie()
    # dict_to_product_model(dottie_result)
    dirty_coins_result = get_dirtycoins()
    dict_to_product_model(dirty_coins_result)
