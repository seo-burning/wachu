
from ic_video import video_update_credential, video_file_update_with_video_source
import sys
import os
import django
import json
import requests
from bs4 import BeautifulSoup
from random import choice
import pymsteams  # https://pypi.org/project/pymsteams/
import time
import datetime

PROJECT_ROOT = os.getcwd()
sys.path.append(os.path.dirname(PROJECT_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.prod")
django.setup()

_user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
]

from product.models import Product, ProductCategory, ProductSubCategory, ProductColor, ProductStyle
from store.models import Store, StorePost, StoreRanking, PostImage

# dateInfo = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
dateInfo = datetime.datetime.now().strftime('%Y-%m-%d')

# dateInfo = '2019-07-22'


class InstagramScraper:

    def __init__(self, user_agents=None, proxy=None):
        self.user_agents = user_agents
        self.proxy = proxy

    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(_user_agents)

    def __request_url(self, url):
        try:
            response = requests.get(url, headers={'User-Agent': self.__random_agent()},
                                    proxies={'http': self.proxy, 'https': self.proxy})
            response.raise_for_status()
        except requests.HTTPError as e:
            status_code = e.response.status_code
            return(status_code)
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response.text

    @staticmethod
    def extract_json_data(html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace(
            'window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)

    def profile_page_metrics(self, profile_url):
        results = {}
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
        except Exception as e:
            pass
        else:
            for key, value in metrics.items():
                if value and isinstance(value, dict):
                    value = value['count']
                    results[key] = value
                elif value:
                    results[key] = value
        return results

    def profile_page_recent_posts(self, profile_url):
        results = []
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']["edges"]
        except Exception as e:
            print("Failed in Posts {} {}".format(profile_url, e))
            pass
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node)
        return results

    def get_content_from_post_page(self, request_url):
        results = []
        try:
            response = self.__request_url(request_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
        except Exception as e:
            print("Failed in Posts {} {}".format(request_url, e))
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node)
        return results

    def check_is_deleted(self, request_url):
        is_deleted = False
        try:
            response = self.__request_url(request_url)
            json_data = self.extract_json_data(response)
        except Exception as e:
            print("Failed in Posts {} {}".format(request_url, e))
            response = self.__request_url(request_url)
            if(response == 404):
                print('404 Error, no post')
                is_deleted = True
            if(response == 502):
                time.sleep(100)
        return is_deleted

    def get_video_from_post_page(self, request_url):
        results = []
        try:
            response = self.__request_url(request_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        except Exception as e:
            print("Failed in Posts {} {}".format(request_url, e))
        return metrics

    def re_update_everything(self, obj_post):
        post_url = obj_post.post_url
        try:
            is_deleted = self.check_is_deleted(
                post_url)
            if is_deleted == True:
                print('deleted')
                obj_post.delete()
            # else:
            #     if obj_post.post_type == 'V':
            #         print('video updated')
            #         post_video = self.get_video_from_post_page(
            #             post_url)
            #         # time.sleep(10)
            #         # obj_post.post_thumb_image = post_video['display_resources'][0]['src']
            #         # obj_post.video_source = post_video['video_url']
            #         video_file_update_with_video_source(
            #             obj_post, post_video['video_url'], post_video['display_resources'][0]['src'])
            #         obj_post.view_count = post_video['video_view_count']
            #         obj_post.save()
            #     if obj_post.post_type == 'MP':
            #         print('multiple post updated')
            #         for obj_old_post in obj_post.post_image_set.all():
            #             obj_old_post.delete()
            #         post_images = self.get_content_from_post_page(post_url)
            #         time.sleep(10)
            #         obj_post.post_thumb_image = post_images[0]['display_resources'][0]['src']
            #         obj_post.save()
            #         for image in post_images:
            #             obj_image, image_is_created = PostImage.objects.get_or_create(
            #                 source=image['display_url'],
            #                 source_thumb=image['display_resources'][0]['src'],
            #                 store_post=obj_post,
            #                 post_image_type='P')
            #             if image['__typename'] == 'GraphVideo':
            #                 print('Video Post')
            #                 obj_image.post_image_type = 'V'
            #                 obj_image.source = image['video_url']
            #                 obj_image.save()

        except Exception as e:
            print(e)

# # 특정 계정 좋아요한 스토어만 남기기
# import csv
# with open('crawling/190927_storelist.csv', 'r') as f:
#     print('read_lines')
#     lines = f.readlines()

# store_list = csv.reader(lines)
# for store in store_list:
#     store_name = store[3]
#     print(store_name)
#     try:
#         store_obj = Store.objects.get(insta_id=store_name)
#         store_obj.is_active=True
#         store_obj.save()
#     except:
#         pass


def deactive_post_by_store(obj_store):
    obj_list = StorePost.objects.all().filter(
        is_active=True).filter(store=obj_store)
    print(obj_store, obj_list.count())
    for i, obj_post in enumerate(obj_list):
        obj_post.is_active = False
        obj_post.save()



# def auto_create():




def categoooo(store_post_obj):
    obj = InstagramScraper()
    obj.re_update_everything(store_post_obj)

# 자주 포스트를 지우는 계정 리스트 확인.
if __name__ == '__main__':
    start_time = time.time()

    import multiprocessing as mp
    from functools import partial
    pool = mp.Pool(processes=6)

    store_list = Store.objects.all().filter(is_active=True).order_by('current_ranking').reverse()[36:]
    print (store_list.count())
    for store_obj in store_list:
        print(store_obj, store_obj.current_ranking)
        store_post_list = StorePost.objects.all().filter(store=store_obj)
        pool.map(categoooo, store_post_list)

    # store_obj = Store.objects.all().get(insta_id='vananhscarlet')
    # store_post_list = StorePost.objects.all().filter(store=store_obj).filter(product=None,is_product='P')
    # post_category = ProductCategory.objects.all().get(name='dress')
    # sub = ProductSubCategory.objects.all().get(name='party_dress')
    # # color_p = ProductColor.objects.all().get(name='black')
    # style= ProductStyle.objects.all().get(name='sexy')

    # print(store_post_list.count())
    # print(sub,style,post_category)
    # for store_post_obj in store_post_list:
    #     product_obj, is_created = Product.objects.get_or_create(store=store_obj, post=store_post_obj, category=post_category, sub_category=sub,style=style)
    #     product_obj.save()
    #     break
    # # print("--- %s seconds ---" % (time.time() - start_time))

