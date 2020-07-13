from homepage.fivetheway import get_5theway
from homepage.dottie import get_dottie
from dosiin.dosiin_crawling import get_dosiin
from homepage.inventory_version import get_olv, get_clothesbar, get_nowsaigon, get_hades, get_dirtycoins,  \
    get_degrey, get_libeworkshop, get_swe, get_blvck, get_tsun, get_tatichubeyoung, get_edini,\
    get_heyyoustudio, get_errorist, get_fusionism, get_shebyshj, get_cecicela, get_lepoulet, get_colin, get_devons
from dict_to_db import dict_to_product_model, dict_to_store_model


def update_homepage():
    # # fivetheway_result = get_5theway()
    # dict_to_store_model(dosiin_brand)
    # dosiin_result = get_dosiin()
    # dict_to_product_model(dosiin_result)
    home_page_list = [get_edini,
                      # get_devons,
                      #                   get_olv, get_tsun,
                      #                   get_lepoulet, get_clothesbar, get_nowsaigon, get_hades, get_dirtycoins,
                      #                   get_degrey, get_libeworkshop, get_swe, get_blvck, get_tatichubeyoung,


                      get_heyyoustudio, get_errorist, get_fusionism, get_shebyshj, get_cecicela, get_colin,
                      ]

    for home_page_obj in home_page_list:
        product_list = home_page_obj()
        dict_to_product_model(product_list)


if __name__ == '__main__':
    update_homepage()
    # check_delete()
    pass
