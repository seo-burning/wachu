from degrey.degrey import degrey_crawler
from homepage.swe import get_swe
from homepage.fivetheway import get_5theway
from homepage.hades import get_hades

from dict_to_db import dict_to_product_model

if __name__ == '__main__':
    print('start scrapying')
    # degrey_result = degrey_crawler()
    # swe_result = get_swe()
    # fivetheway_result = get_5theway()
    hades_result = get_hades()
    dict_to_product_model(hades_result)
