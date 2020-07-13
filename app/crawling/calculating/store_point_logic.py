import datetime


def calculate_post_point(post_like, post_comment, post_taken_at_timestamp):
    """
    Ranking Point Logic
    기본 post_point = > 포스팅의 좋아요 수 + 포스팅의 댓글 수  * commet_addition_ratio(댓글 가산점)
    최근 포스팅 가산점 => 계산 시점과 포스팅 작성일 사이의 차이 일수에서 최대 (recent_post_date - 1)일까지 가산 제공
    최근 포스팅 가산 비율 => recent_post_addition_ratio

    예시
    commet_addition_ratio = 1.3
    recent_post_addition_ratio =0.6
    recent_post_date = 4

    어제 작성된 글의 좋아요 20개 댓글 20개

    post_point = 20 + 20*1.3 = 46 point
    최근 포스팅 가산점 => 최근 3일(recent_post_date - 1)의 포스팅까지 가산점 제공,
     어제 작성된 글의 경우 3의 가산 일자
    최근 포스팅 가산 비율 => 최종 포스팅 포인트의 경우 post_point * 3 * 0.6 = 46 * 1.8 = 82.8 POINT

    5일전 작성된 글의 좋아요 32개 댓글 3개
    post_point = 32 + 3*1.3 = 35.9 POINT
    최근 포스팅 가산 => 3일보다 크기 때문에 없음
    """
    post_point = 0
    commet_addition_ratio = 1.3  # 댓글 가산 포인트 (좋아요 대비)
    recent_post_addition_ratio = 0.55
    recent_post_date = 3  # days from today

    post_point = post_like + post_comment * commet_addition_ratio
    str_timestamp = datetime.datetime.fromtimestamp(
        post_taken_at_timestamp)-datetime.datetime.now()\
        + datetime.timedelta(days=recent_post_date)
    day_adjustment_factor = str_timestamp.days
    if (day_adjustment_factor <= 1):  # 차이가 1일 때부터는 가산비율을 적용 안함
        return post_point
    else:
        return post_point * day_adjustment_factor * recent_post_addition_ratio


def calculate_store_point(post_score_sum, follower, follow, post_num):
    post_score_addition_ratio = 1
    follower_addition_ratio = 1
    follow_addition_ratio = 0.4
    post_num_addtion_ratio = 0.5

    total_score = post_score_sum*post_score_addition_ratio + follower * \
        follower_addition_ratio + follow*follow_addition_ratio + \
        post_num*post_num_addtion_ratio
    return total_score
