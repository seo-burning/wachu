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

# crontab          4      8        12      19      0
#    =>
# 실제시간          11      15       19       2       7
#               0~100   100~끝    0~100     V     100~끝
    if at_time == 4 or at_time == 12:
        slack_notify('*update data @' + date+'*')
        # 쇼피 앞 절반 생성 / 홈페이지 생성
        slack_notify('*update homepage @' + date+'*')
        update_homepage()
        slack_notify('*update shopee 0 ~ 100 @' + date+'*')
        update_shopee(0, 100)
        slack_notify('*calculating @' + date+'*')
        calculating()
        preview_image_update()
        slack_notify('*update data @' + date + '*' + 'done')
    elif at_time == 8 or at_time == 0:
        slack_notify('*update data @' + date+'*')
        slack_notify('*update homepage @' + date+'*')
        update_homepage()
        slack_notify('*update shopee @' + date+'*')
        update_shopee(100)
        slack_notify('*calculating @' + date+'*')
        calculating()
        preview_image_update()
        slack_notify('*update data @' + date+'*' + 'done')
    else:  # 29시에 진행되는 크롤링 (05:00)  상품 검증
        slack_notify('*validate data @' + date+'*')
        slack_notify('*validate homepage @' + date+'*')
        validate_homepage()
        slack_notify('*validate shopee @' + date+'*')
        validate_shopee()
        slack_notify('*calculating @' + date+'*')
        calculating()
        preview_image_update()
        slack_notify('*update data @' + date+'*' + 'done')

    slack_notify("--- %s seconds ---" % (time.time() - start_time))
