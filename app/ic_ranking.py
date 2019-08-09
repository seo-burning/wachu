from store_point_logic import calculate_post_point, calculate_store_point

import sys
import os
import django
import datetime
import time
import multiprocessing as mp
from functools import partial


PROJECT_ROOT = os.getcwd()
sys.path.append(os.path.dirname(PROJECT_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.prod")
django.setup()

from store.models import Store, StorePost, StoreRanking, PostImage

# dateInfo = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
# dateInfo = datetime.datetime.now().strftime('%Y-%m-%d')
dateInfo = '2019-08-09'


def calculate_ranking(store_ranking_obj, all_store_ranking_objs_for_today):
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


if __name__ == '__main__':
    print('calculating Ranking')
    start_time = time.time()

    print('setup multiprocessing')
    pool = mp.Pool(processes=6)

    all_store_ranking_objs_for_today = StoreRanking.objects.filter(
        date=dateInfo).filter(store__is_active=True)

    print(len(all_store_ranking_objs_for_today))
    pool.map(partial(calculate_ranking,
                     all_store_ranking_objs_for_today=all_store_ranking_objs_for_today), all_store_ranking_objs_for_today)

    pool.close()

    print("--- %s seconds ---" % (time.time() - start_time))
