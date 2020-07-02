from homepage.degrey import get_degrey
from homepage.swe import get_swe
from homepage.fivetheway import get_5theway
from homepage.hades import get_hades
from homepage.dottie import get_dottie
from homepage.dirtycoins import get_dirtycoins
from homepage.nowsaigon import get_nowsaigon
from homepage.tatichichubeyoung import get_tatichichubeyoung
from dosiin.dosiin_crawling import get_dosiin
from homepage.libeworkshop import get_libeworkshop
from homepage.shebyshj import get_shebyshj
from homepage.fusionism import get_fusionism
from homepage.tsun import get_tsun
from homepage.xxme import get_xxme
from homepage.errorist import get_errorist
from homepage.cecicela import get_cecicela
from homepage.edini import get_edini
from homepage.heyyoustudio import get_heyyoustudio
from dict_to_db import dict_to_product_model, dict_to_store_model, temp, check_delete

if __name__ == '__main__':
    print('start scrapying')
    # # fivetheway_result = get_5theway()

    # dict_to_store_model(dosiin_brand)
    # dosiin_result = get_dosiin()
    # dict_to_product_model(dosiin_result)
    # # dottie_result = get_dottie()
    # # dict_to_product_model(dottie_result)

    # not organized
    degrey_result = get_degrey()
    dict_to_product_model(degrey_result)
    hades_result = get_hades()
    dict_to_product_model(hades_result)

    # type json
    nowsaigon_result = get_nowsaigon()
    dict_to_product_model(nowsaigon_result)
    tatichichubeyoung_result = get_tatichichubeyoung()
    dict_to_product_model(tatichichubeyoung_result)
    shebyshj_result = get_shebyshj()
    dict_to_product_model(shebyshj_result)
    fusionism_result = get_fusionism()
    dict_to_product_model(fusionism_result)
    # dirty_coins_result = get_dirtycoins()
    # dict_to_product_model(dirty_coins_result)
    tsun_result = get_tsun()
    dict_to_product_model(tsun_result)
    xxme_result = get_xxme()
    dict_to_product_model(xxme_result)
    errorist_result = get_errorist()
    dict_to_product_model(errorist_result)
    cecicela_result = get_cecicela()
    dict_to_product_model(cecicela_result)
    edini_result = get_edini()
    dict_to_product_model(edini_result)
    heyyoustudio_result = get_heyyoustudio()
    dict_to_product_model(heyyoustudio_result)
    libeworkshop_result = get_libeworkshop()
    dict_to_product_model(libeworkshop_result)
    swe_result = get_swe()
    dict_to_product_model(swe_result)
    check_delete()
