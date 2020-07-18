import datetime

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
    time = int(datetime.datetime.now().strftime('%I'))

    if time < 6:
        slack_notify('*update data @' + date+'*')
        # 새벽 생성
        slack_notify('*update shopee @' + date+'*')
        update_shopee()
        slack_notify('*update homepage @' + date+'*')
        update_homepage()
        slack_notify('*calculating @' + date+'*')
        calculating()
        preview_image_update()
        slack_notify('*update data @' + date+'*' + 'done')
    else:
        slack_notify('*update(validate) data @' + date+'*')
        # 오후 삭제
        slack_notify('*update(validate)  shopee @' + date+'*')
        validate_shopee()
        slack_notify('*update(validate)  homepage @' + date+'*')
        validate_homepage()
        slack_notify('*calculating @' + date+'*')
        calculating()
        preview_image_update()
        slack_notify('*update(validate) data @' + date+'*' + 'done')
