import datetime

from shopee_c import update_shopee, validate_shopee
from point_calculating import calculate_store_review_rating, \
    calculate_product_review_rating, calculate_store_point

from dict_to_db import validate_homepage
from homepage_c import update_homepage
from utils.slack import slack_notify


def calculating():
    calculate_product_review_rating()
    calculate_store_review_rating()
    calculate_store_point()


if __name__ == '__main__':
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    time = int(datetime.datetime.now().strftime('%I'))
    slack_notify('*update data @' + date+'*')

    if time < 6:
        # 새벽 생성
        update_shopee()
        update_homepage()
        calculating()
    else:
        # 오후 삭제
        validate_shopee()
        validate_homepage()
        calculating()
