from homepage.degrey import get_degrey
from homepage.swe import get_swe
from homepage.fivetheway import get_5theway
from homepage.hades import get_hades

from dict_to_db import dict_to_product_model

if __name__ == '__main__':
    print('start scrapying')
    # degrey_result = get_degrey()
    # dict_to_product_model(degrey_result)
    swe_result = get_swe()
    dict_to_product_model(swe_result)
    # fivetheway_result = get_5theway()
    hades_result = get_hades()
    dict_to_product_model(hades_result)
