import datetime
import time

from shopee_c import update_shopee, validate_shopee
from point_calculating import calculate_store_review_rating, \
    calculate_product_review_rating, calculate_store_point
from manual_update import preview_image_update
from homepage_c import update_homepage, validate_homepage
from utils.slack import slack_notify


def calculating():
    calculate_product_review_rating()
    calculate_store_review_rating()
    calculate_store_point()


if __name__ == '__main__':
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:00')
    at_time = int(datetime.datetime.now().strftime('%H'))
    start_time = time.time()

    if at_time > 18:  # 25시에 진행되는 크롤링 (01:00)        # 쇼피 뒤 절반 생성 / 홈페이지 업데이트
        slack_notify('*update data @' + date+'*')
        # 쇼피 앞 절반 생성 / 홈페이지 생성
        slack_notify('*update homepage @' + date+'*')
        update_homepage()
        slack_notify('*update shopee 0 ~ 100 @' + date+'*')
        update_shopee(0, 100)
        slack_notify('*calculating @' + date+'*')
        calculating()
        preview_image_update()
        slack_notify('*update data @' + date+'*' + 'done')
    elif at_time > 22:  # 29시에 진행되는 크롤링 (05:00)  상품 검증
        slack_notify('*validate data @' + date+'*')
        slack_notify('*validate homepage @' + date+'*')
        validate_homepage()
        slack_notify('*validate shopee @' + date+'*')
        validate_shopee()
        slack_notify('*calculating @' + date+'*')
        calculating()
        preview_image_update()
        slack_notify('*update data @' + date+'*' + 'done')
    elif at_time > 7:  # 14시 진행되는 크롤링         # 홈페이지 신규 상품 생성 / 쇼피 앞 절반 생성
        slack_notify('*update data @' + date+'*')
        slack_notify('*update homepage @' + date+'*')
        update_homepage()
        slack_notify('*update shopee @' + date+'*')
        update_shopee(100)
        slack_notify('*calculating @' + date+'*')
        calculating()
        preview_image_update()
        slack_notify('*update data @' + date+'*' + 'done')
    slack_notify("--- %s seconds ---" % (time.time() - start_time))
