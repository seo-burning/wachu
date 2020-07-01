import datetime

from shopee_c import update_shopee
from instagram_c import update_instagram
from point_calculating import calculate_store_review_rating, \
    calculate_product_review_rating, calculate_store_point

from utils.slack import slack_notify


if __name__ == '__main__':
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    slack_notify('_daily update execute_ @'+date)

    # slack_notify('*product review rating update*')
    # calculate_product_review_rating()
    # slack_notify('*store review rating update*')
    # calculate_store_review_rating()
    slack_notify('*store point update and calculate ranking*')
    calculate_store_point()
    slack_notify('_daily update done_ @'+date)

    # slack_notify('*instagram update*')
    # update_instagram()
    # slack_notify('*shopee update*')
    update_shopee()

    # check deactivated item.
