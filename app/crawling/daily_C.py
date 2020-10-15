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


def first_set(group_name):
    slack_notify('>'+group_name+' homepage & shopee 145~')
    update_homepage()
    slack_notify('>'+group_name+' update homepage complete')
    update_shopee(145)
    slack_notify('>'+group_name+' update shopee 145 ~ complete')


def second_set(group_name):
    slack_notify('>'+group_name+' shopee 70 ~ 145')
    update_shopee(70, 145)
    slack_notify('>'+group_name+' update shopee 70~145 complete')


def third_set(group_name):
    slack_notify('>'+group_name+' shopee 0 ~ 70 & calculating')
    update_shopee(0, 70)
    slack_notify('>' + group_name + ' update shopee 0~70 complete & start caculating')
    validate_homepage()
    calculating()
    preview_image_update()
    slack_notify('>'+group_name+' calculating & thumb update ~ complete')


def validate_set(group_name):
    slack_notify('>'+group_name+' shopee 100 ~ ')
    update_shopee(100)
    slack_notify('>'+group_name+' update shopee ~100 complete')


if __name__ == '__main__':
    while True:
        group_name = 'C'
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:00')
        at_time = int(datetime.datetime.now().strftime('%H'))
        start_time = time.time()
        slack_notify(group_name + date + '*')
        type_A = [2, 9, 15]
        type_B = [4, 11, 17]
        type_C = [7, 9, 24]
        # if at_time in type_A:
        third_set(group_name)
        # elif at_time in type_B:
        #     first_set(group_name)
        # elif at_time in type_C:
        #     second_set(group_name)
        # else:
        #     validate_set(group_name)
        slack_notify("--- %s seconds ---" % (time.time() - start_time))
        slack_notify(group_name + " complete")
