import os_setup
from product.models import Product, ShopeeRating, ProductImage, ShopeeCategory, ProductSize, ProductColor, ProductExtraOption, ProductOption, ShopeeColor, ShopeeSize, ProductBackEndRate
from store.models import Store, StorePost, StoreRanking
from user.models import ProductReview

from datetime import datetime, timezone, timedelta
import multiprocessing as mp

dateInfo = (datetime.now()).strftime('%Y-%m-%d')


def _calculate_store_point(store_obj):
    follower = store_obj.follower * 0.2
    product_list = Product.objects.filter(store=store_obj)
    product_rate_sum = 0
    for product_obj in product_list:
        product_rate_sum += product_obj.current_product_backend_rating / 100
    product_count = len(product_list)
    favorite_count = store_obj.favorite_users.count()
    total_score = follower + float(product_rate_sum * product_count) + favorite_count*10

    obj_store_ranking, ranking_is_created = StoreRanking.objects.get_or_create(
        store=store_obj, date=dateInfo
    )
    if ranking_is_created:
        print(ranking_is_created)
    obj_store_ranking.date = dateInfo
    obj_store_ranking.post_total_score = float(product_rate_sum * product_count)
    obj_store_ranking.follower = store_obj.follower
    obj_store_ranking.following = store_obj.favorite_users.count()
    obj_store_ranking.post_num = product_count
    obj_store_ranking.store_score = total_score
    obj_store_ranking.review_rating = store_obj.current_review_rating
    obj_store_ranking.store_view_count = 0

    obj_store_ranking.save()

    print(store_obj.insta_id, total_score, follower, product_rate_sum,
          product_count, product_rate_sum * product_count, favorite_count)
    return total_score


def _calculate_ranking(store_ranking_obj, all_store_ranking_objs_for_today):
    ranking = all_store_ranking_objs_for_today.filter(
        store_score__gt=store_ranking_obj.store_score).count()+1
    store_ranking_obj.ranking = ranking
    try:
        previous_ranking = list(StoreRanking.objects.filter(
            store=store_ranking_obj.store))[-2]
        store_ranking_obj.ranking_changed = previous_ranking.ranking - ranking
        print(store_ranking_obj.ranking_changed)
    except:
        store_ranking_obj.ranking_changed = 99999
        print('calculate_failed')

    store_ranking_obj.save()
    store_ranking_obj.store.current_ranking = store_ranking_obj.ranking
    store_ranking_obj.store.current_ranking_changed = store_ranking_obj.ranking_changed
    store_ranking_obj.store.save()


def calculate_store_point():
    store_list = Store.objects.filter(is_active=True)
    print(len(store_list))
    for store_obj in store_list:
        store_score = _calculate_store_point(store_obj)
    all_store_ranking_objs_for_today = StoreRanking.objects.filter(
        date=dateInfo).filter(store__is_active=True)
    print(len(all_store_ranking_objs_for_today))
    for store_ranking_obj in all_store_ranking_objs_for_today:
        store_score = _calculate_ranking(store_ranking_obj, all_store_ranking_objs_for_today)


def calculating_product_obj_rating(product_obj, default=None):
    shopee_review_count = 0
    shopee_review_rate = 0
    shopee_view_count = 0
    shopee_liked_count = 0
    shopee_sold_count = 0
    review_score = 0
    post_like = 0
    post_comment = 0
    app_click_count = 0
    app_outlink_count = 0
    user_favorite_count = 0
    product_infomation_quality = 0
    review_count = 0
    review_rate = 0
    if default:
        total_score = 250
    else:
        if product_obj.product_source == 'SHOPEE':
            shopee_rating_obj = ShopeeRating.objects.get(product=product_obj)
            shopee_review_count = shopee_rating_obj.shopee_review_count
            shopee_review_rate = shopee_rating_obj.shopee_rating_star
            shopee_view_count = shopee_rating_obj.shopee_view_count / 100
            shopee_liked_count = shopee_rating_obj.shopee_liked_count / 4
            shopee_sold_count = shopee_rating_obj.shopee_sold_count / 3
        review_score = shopee_review_count*shopee_review_rate / 3
        if review_score > 70:
            review_score = 70
        if shopee_view_count > 70:
            shopee_view_count = 70
        if shopee_liked_count > 70:
            shopee_liked_count = 70
        if shopee_sold_count > 70:
            shopee_sold_count = 70
        shopee_total_score = review_score + \
            shopee_view_count + shopee_liked_count + shopee_sold_count

        if product_obj.post:
            post_like = product_obj.post.post_like / 30
            post_comment = product_obj.post.post_comment * 5
        post_total_score = post_like + post_comment
        review_list = ProductReview.objects.filter(product=product_obj)

        for review_obj in review_list:
            review_count = review_count + 1
            review_rate = review_rate + review_obj.rating
        review_total_score = review_count * review_rate

        total_score = shopee_total_score + post_total_score + review_total_score
        if total_score > 999:
            total_score = 999

    product_rate_obj, is_created = ProductBackEndRate.objects.get_or_create(product=product_obj)
    product_rate_obj.shopee_review_count = shopee_review_count
    product_rate_obj.shopee_review_rate = shopee_review_rate
    product_rate_obj.shopee_view_count = shopee_view_count
    product_rate_obj.shopee_liked_count = shopee_liked_count
    product_rate_obj.shopee_sold_count = shopee_sold_count
    product_rate_obj.post_like = post_like
    product_rate_obj.post_comment = post_comment
    product_rate_obj.review_count = review_count
    product_rate_obj.review_rate = review_rate

    created_at = product_obj.created_at
    time_diff = created_at - datetime.now(timezone.utc)
    if time_diff.days > -2:
        total_score = total_score*1.5
    elif time_diff.days < -7:
        total_score = total_score/2
    elif time_diff.days < -30:
        total_score = total_score/3
    elif time_diff.days < -60:
        total_score = total_score/4
    elif time_diff.days < -90:
        total_score = total_score/6

    product_rate_obj.product_backend_rating = total_score
    product_obj.current_product_backend_rating = total_score
    product_obj.save()
    print(total_score, review_score, shopee_view_count, shopee_liked_count, shopee_sold_count, post_like, post_comment)
    product_rate_obj.save()
    return (total_score, review_score, shopee_view_count, shopee_liked_count, shopee_sold_count, post_like, post_comment)


def calculating_product_obj_rating(product_obj):
    shopee_review_count = 0
    shopee_review_rate = 0
    shopee_view_count = 0
    shopee_liked_count = 0
    shopee_sold_count = 0
    review_score = 0
    post_like = 0
    post_comment = 0
    app_click_count = 0
    app_outlink_count = 0
    user_favorite_count = 0
    product_infomation_quality = 0
    review_count = 0
    review_rate = 0
    if product_obj.product_source == 'SHOPEE':
        shopee_rating_obj = ShopeeRating.objects.get(product=product_obj)
        shopee_review_count = shopee_rating_obj.shopee_review_count
        shopee_review_rate = shopee_rating_obj.shopee_rating_star
        shopee_view_count = shopee_rating_obj.shopee_view_count / 100
        shopee_liked_count = shopee_rating_obj.shopee_liked_count / 4
        shopee_sold_count = shopee_rating_obj.shopee_sold_count / 3
    review_score = shopee_review_count*shopee_review_rate / 3
    if review_score > 70:
        review_score = 70
    if shopee_view_count > 70:
        shopee_view_count = 70
    if shopee_liked_count > 70:
        shopee_liked_count = 70
    if shopee_sold_count > 70:
        shopee_sold_count = 70
    shopee_total_score = review_score + \
        shopee_view_count + shopee_liked_count + shopee_sold_count

    if product_obj.post:
        post_like = product_obj.post.post_like / 30
        post_comment = product_obj.post.post_comment * 5
    post_total_score = post_like + post_comment
    review_list = ProductReview.objects.filter(product=product_obj)

    for review_obj in review_list:
        review_count = review_count + 1
        review_rate = review_rate + review_obj.rating
    review_total_score = review_count * review_rate

    total_score = shopee_total_score + post_total_score + review_total_score
    if total_score > 999:
        total_score = 999

    product_rate_obj, is_created = ProductBackEndRate.objects.get_or_create(product=product_obj)
    product_rate_obj.shopee_review_count = shopee_review_count
    product_rate_obj.shopee_review_rate = shopee_review_rate
    product_rate_obj.shopee_view_count = shopee_view_count
    product_rate_obj.shopee_liked_count = shopee_liked_count
    product_rate_obj.shopee_sold_count = shopee_sold_count
    product_rate_obj.post_like = post_like
    product_rate_obj.post_comment = post_comment
    product_rate_obj.review_count = review_count
    product_rate_obj.review_rate = review_rate

    created_at = product_obj.created_at
    time_diff = created_at - datetime.now(timezone.utc)
    if time_diff.days > -2:
        total_score = total_score*1.5
    elif time_diff.days < -7:
        total_score = total_score/2
    elif time_diff.days < -30:
        total_score = total_score/3
    elif time_diff.days < -60:
        total_score = total_score/4
    elif time_diff.days < -90:
        total_score = total_score/6

    product_rate_obj.product_backend_rating = total_score
    product_obj.current_product_backend_rating = total_score
    product_obj.save()
    product_rate_obj.save()
    return (total_score, review_score, shopee_view_count, shopee_liked_count, shopee_sold_count, post_like, post_comment)


def calculating_product_list_rating_with_default(product_obj):
    total_score = 250
    product_rate_obj, is_created = ProductBackEndRate.objects.get_or_create(product=product_obj)
    created_at = product_obj.created_at
    time_diff = created_at - datetime.now(timezone.utc)
    if time_diff.days > -2:
        total_score = total_score*1.5
    elif time_diff.days < -7:
        total_score = total_score/2
    elif time_diff.days < -30:
        total_score = total_score/3
    elif time_diff.days < -60:
        total_score = total_score/4
    elif time_diff.days < -90:
        total_score = total_score/6
    product_rate_obj.product_backend_rating = total_score
    product_obj.current_product_backend_rating = total_score
    product_obj.save()
    product_rate_obj.save()
    return (total_score)


def calculating_product_list_rating(product_list):
    review_score_sum = 0
    shopee_view_count_sum = 0
    shopee_liked_count_sum = 0
    shopee_sold_count_sum = 0
    post_like_sum = 0
    post_comment_sum = 0
    total_score_sum = 0
    review_score_top = 0
    shopee_view_count_top = 0
    shopee_liked_count_top = 0
    shopee_sold_count_top = 0
    post_like_top = 0
    post_comment_top = 0
    total_score_top = 0
    i = 0
    for product_obj in product_list:
        total_score, review_score, shopee_view_count, shopee_liked_count, shopee_sold_count, post_like, post_comment = calculating_product_obj_rating(
            product_obj)
        review_score_sum += review_score
        shopee_view_count_sum += shopee_view_count
        shopee_liked_count_sum += shopee_liked_count
        shopee_sold_count_sum += shopee_sold_count
        post_like_sum += post_like
        post_comment_sum += post_comment
        total_score_sum += total_score
        if review_score > review_score_top:
            review_score_top = review_score
        if shopee_view_count > shopee_view_count_top:
            shopee_view_count_top = shopee_view_count
        if shopee_liked_count > shopee_liked_count_top:
            shopee_liked_count_top = shopee_liked_count
        if shopee_sold_count > shopee_sold_count_top:
            shopee_sold_count_top = shopee_sold_count
        if post_like > post_like_top:
            post_like_top = post_like
        if post_comment > post_comment_top:
            post_comment_top = post_comment
        if total_score > total_score_top:
            total_score_top = total_score
        i += 1
    print(total_score_sum/i, review_score_sum/i, shopee_view_count_sum/i,
          shopee_liked_count_sum/i, shopee_sold_count_sum/i, post_like_sum/i, post_comment_sum/i)
    print('top', total_score_top, review_score_top, shopee_view_count_top,
          shopee_liked_count_top, shopee_sold_count_top, post_like_top, post_comment_top)

# Product Review


def _calculating_product_obj_review_rating(product_obj):
    product_point = 0
    review_count = 0
    if product_obj.product_source == 'SHOPEE':
        shopee_rating_obj = ShopeeRating.objects.get(product=product_obj)
        review_count = shopee_rating_obj.shopee_review_count
        product_point = shopee_rating_obj.shopee_rating_star * review_count
    review_list = ProductReview.objects.filter(product=product_obj)
    for review_obj in review_list:
        review_count = review_count + 1
        product_point = product_point + review_obj.rating
    if review_count > 0:
        product_rating = product_point / review_count
        product_obj.current_review_rating = product_rating
        product_obj.save()
    else:
        product_rating = 0
        product_obj.current_review_rating = 0
        product_obj.save()


def _calculate_store_obj_review_rating(store_obj):
    store_point = 0
    review_count = 0
    current_review_rating = 0
    product_list = Product.objects.filter(store=store_obj)

    for product_obj in product_list:
        if product_obj.current_review_rating > 0:
            store_point += product_obj.current_review_rating
            review_count += 1
    if review_count > 0:
        current_review_rating = store_point / review_count
        store_obj.current_review_rating = current_review_rating
    store_obj.save()


# Export Functions
def calculate_product_review_rating():
    product_list = Product.objects.all()
    print('Calculating product review rating....')
    pool = mp.Pool(processes=6)
    print('Set up Multiprocessing....')
    pool.map(_calculating_product_obj_review_rating, product_list)
    pool.close()


def calculate_store_review_rating():
    store_list = Store.objects.filter(is_active=True)
    print('Calculating product review rating....')
    pool = mp.Pool(processes=6)
    print('Set up Multiprocessing....')
    pool.map(_calculate_store_obj_review_rating, store_list)
    pool.close()
