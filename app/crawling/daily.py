import datetime

from shopee_c import update_shopee, validate_shopee
from point_calculating import calculate_store_review_rating, \
    calculate_product_review_rating, calculate_store_point
from homepage_c import update_homepage
from utils.slack import slack_notify


if __name__ == '__main__':
    # date = datetime.datetime.now().strftime('%Y-%m-%d')
    # slack_notify('_daily update execute_ @'+date)
    # update_homepage()
    # slack_notify('*product review rating update*')
    # calculate_product_review_rating()
    # slack_notify('*store review rating update*')
    # calculate_store_review_rating()
    # slack_notify('*store point update and calculate ranking*')
    # calculate_store_point()
    # slack_notify('_daily update done_ @'+date)
    # slack_notify('*instagram update*')
    # update_instagram()

    # check deactivated item.
    # 새벽 생성
    # slack_notify('*shopee update*')
    # update_shopee()
    # 오후 삭제
    validate_shopee()
