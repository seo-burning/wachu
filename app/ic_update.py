
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
from ic_video import video_update_credential, video_file_update_with_video_source

PROJECT_ROOT = os.getcwd()
sys.path.append(os.path.dirname(PROJECT_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.prod")
django.setup()
from store.models import Store, StorePost, StoreRanking, PostImage

_user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
]


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
            print(e)
            pass
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
            is_deleted = True
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

    def re_update_everything(self, obj_post, file):
        post_url = obj_post.post_url
        try:
            is_deleted = self.check_is_deleted(
                post_url)
            if is_deleted == True:
                file.write('deleted\n')
                print('deleted')
                obj_post.delete()
            else:
                if obj_post.post_type == 'V':
                    print('video updated')
                    post_video = self.get_video_from_post_page(
                        post_url)
                    # time.sleep(10)
                    # obj_post.post_thumb_image = post_video['display_resources'][0]['src']
                    # obj_post.video_source = post_video['video_url']
                    video_file_update_with_video_source(obj_post, post_video['video_url'], post_video['display_resources'][0]['src'])
                    obj_post.view_count = post_video['video_view_count']
                    obj_post.save()
                if obj_post.post_type == 'MP':
                    print('multiple post updated')
                    for obj_old_post in obj_post.post_image_set.all():
                        obj_old_post.delete()
                    post_images = self.get_content_from_post_page(post_url)
                    time.sleep(10)
                    obj_post.post_thumb_image = post_images[0]['display_resources'][0]['src']
                    obj_post.save()
                    for image in post_images:
                        obj_image, image_is_created = PostImage.objects.get_or_create(
                            source=image['display_url'],
                            source_thumb=image['display_resources'][0]['src'],
                            store_post=obj_post,
                            post_image_type='P')
                        if image['__typename'] == 'GraphVideo':
                            print('Video Post')
                            obj_image.post_image_type = 'V'
                            obj_image.source = image['video_url']
                            obj_image.save()

        except Exception as e:
            print(e)

# 자주 포스트를 지우는 계정 리스트 확인.
if __name__ == '__main__':
    print('start scrapying')
    start_time = time.time()
    with open('crawling/update_result.txt','w') as f:
        obj = InstagramScraper()
        for obj_store in Store.objects.all().filter(is_active=True).order_by('current_ranking')[603:]:
            print('update #{} {}'.format(
                obj_store.current_ranking, obj_store.insta_id))
            f.write('update #{} {}\n'.format(
                obj_store.current_ranking, obj_store.insta_id))
            obj_list = StorePost.objects.all().filter(store=obj_store, post_type='V')
            print(len(obj_list))
            for i, obj_post in enumerate(obj_list):
                obj.re_update_everything(obj_post, f)

    print("--- %s seconds ---" % (time.time() - start_time))
