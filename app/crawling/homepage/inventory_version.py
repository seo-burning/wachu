from . import template


def get_blvck():
    print('\nupdate blvck')
    return template.homepage_crawler("https://blvck-clothing.com",
                                     436, "street", url_list=['all-items'], block_name='product-block')


def get_tsun():
    print('\nupdate tsun')
    return template.homepage_crawler("https://tsunsg.com",
                                     299, "street", url_list=['all'], block_name='product-block')


def get_tatichubeyoung():
    print('\nupdate tatichubeyoung')
    return template.homepage_crawler("https://tatichu.com",
                                     114, "feminine", url_list=['all'])


def get_edini():
    print('\nupdate edini')
    url_list = ['dress', 'skirt', 't-shirts', 'blouse', 'jeans-pants', 'shorts', 'giay']
    return template.homepage_crawler("http://edini.vn",
                                     626,
                                     "feminine",
                                     url_list,
                                     block_name='single-product')


def get_heyyoustudio():
    print('\nupdate heyyoustudio')
    url_list = ['all']
    return template.homepage_crawler("http://heyyoustudio.vn",
                                     637,
                                     "street",
                                     url_list,
                                     block_name='single-product')


def get_errorist():
    print('\nupdate errorist')
    url_list = ['all']
    return template.homepage_crawler("http://errorist.vn",
                                     619,
                                     "sexy",
                                     url_list)


def get_fusionism():
    print('\nupdate fusionism')
    url_list = ['t-shirt', 'long-sleeve',
                'hoodie', 'hoodie-zip', 'sweater',
                'jacket-1', 'gile', 'croptop', 'pants', 'skirt', 'phu-kien', ]
    return template.homepage_crawler("http://fusionism.vn",
                                     307,
                                     "street",
                                     url_list)


def get_swe():
    print('\nupdate swe')
    url_list = [
        'new-arrivals', 'tops',
        'outerwear', 'bottoms', 'accessories']
    return template.homepage_crawler("https://swe.vn",
                                     296,
                                     "street",
                                     url_list,
                                     block_name='single-product')


def get_shebyshj():
    print('\nupdate shebyshj')
    url_list = [
        'all']
    return template.homepage_crawler("https://shebyshj.com",
                                     618,
                                     "sexy",
                                     url_list,
                                     block_name='single-product')


def get_libeworkshop():
    print('\nupdate libeworkshop')
    url_list = ['t-shirt-1', 'shirt-1', 'camisole',
                'bottom', 'skirt', 'dresses-jumpsuits', 'outer-wear', 'swimwear', 'lookbook-home-alone']
    return template.homepage_crawler("https://libeworkshop.com",
                                     9,
                                     "feminine",
                                     url_list, option_type=13)


def get_degrey():
    print('\nupdate degrey')
    url_list = ['tat-ca-san-pham']
    return template.homepage_crawler("https://degrey.vn",
                                     291,
                                     "street",
                                     url_list,)


def get_cecicela():
    print('\nupdate cecicela')
    url_list = ['shirts-blouses', 'tops', 'dres', 'skirts', 'jeans', 'shorts', 'pants']
    return template.homepage_crawler("http://www.cecicela.vn",
                                     620,
                                     "feminine",
                                     url_list,
                                     block_name='single-product')


def get_hades():
    print('\nupdate hades')
    url_list = ['all', ]
    return template.homepage_crawler("https://hades.vn",
                                     293,
                                     "street",
                                     url_list,)


def get_nowsaigon():
    print('\nupdate nowsaigon')
    url_list = ['all', ]
    return template.homepage_crawler("https://nowsaigon.com",
                                     297,
                                     "street",
                                     url_list,
                                     block_name='product-box',
                                     script_string=r'(?<=productJson =).*')


def get_clothesbar():
    print('\nupdate clothesbar')
    url_list = ['all', ]
    return template.homepage_crawler("https://clothesbar.shop",
                                     627, "feminine", url_list)


def get_lepoulet():
    print('\nupdate lepoulet')
    url_list = ['all', ]
    return template.homepage_crawler("https://lepoulet.vn", 52, None,
                                     url_list=['all'], block_name='product-block')


def get_olv():
    print('\nupdate olv')
    url_list = ['tat-ca-san-pham', ]
    return template.homepage_crawler("https://www.olv.vn", 678, 'feminine',
                                     url_list)


# unqualified


def get_classysaigon():
    print('\nupdate nowsaigon')
    return template.homepage_crawler("https://classysg.com",
                                     52,
                                     "street",
                                     url_list=['all'],
                                     block_name='product-box',
                                     script_string=r'(?<=productJson =).*')

#   error cloud flare ddos


def get_dirtycoins():
    print('\nupdate dirtycoins')
    url_list = ['t-shirts-polos', 'longsleeves',
                'shirts', 'sweaters', 'hoodies', 'jackets', 'pants', 'shorts-1', 'caps-hats',
                'wallets-1', 'masks', 'backpacks', 'crossbody-bags', 'messenger-bags', 'shoulder-bags', 'waistbags', ]
    return template.homepage_crawler("http://www.dirtycoins.vn",
                                     294,
                                     "street",
                                     url_list,
                                     block_name='single-product')


# shopee
def get_xxme():
    print('\nupdate xxme')
    url_list = ['all', ]
    return template.homepage_crawler("http://www.xxme.vn",
                                     371,
                                     "street",
                                     url_list,
                                     block_name='product-item')
