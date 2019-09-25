
from store.models import Store, StorePost, StoreRanking, PostImage
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
from store_point_logic import calculate_post_point, calculate_store_point
import multiprocessing as mp
from functools import partial
from time import sleep
import random

from ic_video import video_update_credential, video_file_update_with_video_source


PROJECT_ROOT = os.getcwd()
sys.path.append(os.path.dirname(PROJECT_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.prod")


django.setup()


_user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 6.0; HTC One X10 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'
]


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxy_list = soup.find('tbody')
    proxies = set()
    for rows in proxy_list.find_all('tr')[:5]:
        proxies.add(rows.find_all('td')[0].text +
                    ':'+rows.find_all('td')[1].text)
    return proxies


# dateInfo = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
# dateInfo = datetime.datetime.now().strftime('%Y-%m-%d')
dateInfo = '2019-09-14'


class InstagramScraper:
    def __init__(self, user_agents=None, proxy=None):
        self.user_agents = user_agents
        self.proxy = proxy

    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(_user_agents)

    def __random_proxies(self):
        if self.proxy and isinstance(self.proxy, list):
            print('execute')
            return choice(self.proxy)
        proxies = get_proxies()
        return random.sample(get_proxies(), 1)[0]

    def __request_url(self, url):
        try:
            response = requests.get(url, headers={'user-agent': self.__random_agent(), },
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
            deactivated_account.append(profile_url)
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
            print("Failed in Get Posts {} {}".format(profile_url, e))
            post_error_account.append(profile_url)
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
            print("Failed in Get Single Posts {} {}".format(request_url, e))
            post_error_account.append(request_url)
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node)
        return results

    def get_video_from_post_page(self, request_url):
        results = []
        try:
            response = self.__request_url(request_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        except Exception as e:
            print("Failed in Get Posts'  video{} {}".format(request_url, e))
            post_error_account.append(request_url)
        return metrics

    def insert_insta(self, url, created_account, updated_account, deactivated_account, post_error_account, post_0_account):
        results = {}
        print(url)
        results = self.profile_page_metrics(url)
        sleep(2+random.random()*5)
        result_post = []
        result_post = self.profile_page_recent_posts(url)
        sleep(2+random.random()*5)

        profile_description = ''
        email = ''
        phone = ''
        post_num = ''
        follow = ''
        follower = ''
        username = ''
        fullname = ''
        profile_image = ''
        facebook_url = ''

        if 'username' in results.keys():
            username = results['username']

        if 'full_name' in results.keys():
            fullname = results['full_name']

        if 'edge_follow' in results.keys():
            follow = results['edge_follow']

        if 'edge_followed_by' in results.keys():
            follower = results['edge_followed_by']

        if 'edge_owner_to_timeline_media' in results.keys():
            post_num = results['edge_owner_to_timeline_media']

        if 'biography' in results.keys():
            profile_description = results['biography']

        if 'business_phone_number' in results.keys():
            phone = results['business_phone_number']

        if 'business_email' in results.keys():
            email = results['business_email']

        if 'external_url' in results.keys():
            facebook_url = results['external_url']

        if 'profile_pic_url_hd' in results.keys():
            profile_image = results['profile_pic_url_hd']

        if username:
            obj_store, is_created = Store.objects.get_or_create(
                insta_id=username)
            obj_store.is_updated = True
            obj_store.name = fullname
            obj_store.follower = follower
            obj_store.following = follow
            obj_store.post_num = post_num
            obj_store.description = profile_description + "\n" + facebook_url
            obj_store.phone = phone
            obj_store.email = email
            obj_store.insta_url = 'http://www.instagram.com/' + username + '/'
            obj_store.profile_image = profile_image

            post_saved = 0
            post_score_sum = 0
            is_new_post = False
            if len(result_post) > 0:
                for i, post in enumerate(result_post):
                    post_url = ''
                    post_like = 0
                    post_commnet = 0
                    post_description = ''
                    post_taken_at_timestamp = 0
                    post_score = 0
                    try:
                        post_id = post['id']
                        post_url = 'https://www.instagram.com/p/' + \
                            post['shortcode']
                        post_like = post['edge_liked_by']['count']
                        post_comment = post['edge_media_to_comment']['count']
                        post_taken_at_timestamp = post['taken_at_timestamp']
                        post_thumb_image = post['thumbnail_src']

                        if 'edge_media_to_caption' in post:
                            try:
                                post_description = post['edge_media_to_caption']['edges'][0]['node']['text']
                            except:
                                pass
                        obj_post, post_is_created = StorePost.objects.get_or_create(
                            post_id=post_id, store=obj_store)
                        obj_post.post_like = post_like
                        obj_post.post_url = post_url
                        obj_post.post_description = post_description
                        obj_post.post_comment = post_comment
                        obj_post.post_taken_at_timestamp = post_taken_at_timestamp
                        obj_post.post_thumb_image = post_thumb_image
                        if post_is_created == True:
                            print('{} - #{} new post'.format(obj_store.insta_id, i))
                            is_new_post = True
                            obj_post.is_updated = True
                            if post['__typename'] == 'GraphSidecar':
                                obj_post.post_type = 'MP'
                                post_images = self.get_content_from_post_page(
                                    post_url)
                                sleep(2+random.random()*5)
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

                            elif post['__typename'] == 'GraphVideo':
                                obj_post.post_type = 'V'
                                post_video = self.get_video_from_post_page(
                                    post_url)
                                sleep(2+random.random()*5)
                                video_file_update_with_video_source(
                                    obj_post, post_video['video_url'], post_video['thumbnail_src'])
                                obj_post.view_count = post_video['video_view_count']
                            elif post['__typename'] == 'GraphImage':
                                obj_post.post_type = 'SP'
                                obj_image, image_is_created = PostImage.objects.get_or_create(
                                    source=post['thumbnail_src'],
                                    source_thumb=post['thumbnail_resources'][4]['src'],
                                    store_post=obj_post,
                                    post_image_type='P')
                            else:
                                print('Unknown Type')
                        if i == 0:
                            obj_store.recent_post_1 = obj_post.post_thumb_image
                        elif i == 1:
                            obj_store.recent_post_2 = obj_post.post_thumb_image
                        elif i == 2:
                            obj_store.recent_post_3 = obj_post.post_thumb_image
                        obj_post.post_score = calculate_post_point(
                            post_like, post_comment, post_taken_at_timestamp)
                        obj_post.save()
                        post_saved = post_saved + 1
                        post_score_sum = post_score_sum + obj_post.post_score
                    except IndexError as e:
                        print('E', end='')
                        post_error_account.append(obj_store.insta_url)
                        pass

            else:
                post_0_account.append(obj_store.insta_url)
                print("Fail to Find post. Account may be Private")
            obj_store_ranking, ranking_is_created = StoreRanking.objects.get_or_create(
                store=obj_store, date=dateInfo
            )
            obj_store.is_new_post = is_new_post
            obj_store.save()

            obj_store_ranking.post_total_score = post_score_sum
            obj_store_ranking.follower = follower
            obj_store_ranking.following = follow
            obj_store_ranking.post_num = post_num
            obj_store_ranking.store_score = calculate_store_point(
                post_score_sum, follower, follow, post_num)
            obj_store_ranking.save()

            if (is_created):
                created_account.append(obj_store.insta_url)
                print("C - {} (id:{} / {} post saved.)".format(username,
                                                               obj_store.id, post_saved))
            elif (is_created == False):
                updated_account.append(obj_store.insta_url)
                print("U - {} (id:{} / {} post saved.)".format(username,
                                                               obj_store.id, post_saved))
            time.sleep(1)


if __name__ == '__main__':
    print('start scrapying')
    print(dateInfo)

    start_time = time.time()

    created_account = []
    updated_account = []
    deactivated_account = []
    post_error_account = []
    post_0_account = []

    print('get crawlinglist')
    with open('crawling/account_list.txt', 'r') as f:
        content = f.readlines()
    all_store_ranking_objs_for_today = StoreRanking.objects.filter(
        date=dateInfo).filter(store__is_active=True)
    print(len(all_store_ranking_objs_for_today))
    store_list = Store.objects.all().filter(
        is_active=True).order_by('current_ranking')[525:]
    print(len(store_list))
    content = ['https://www.instagram.com/' +
               x.insta_id + '/' for x in store_list]
    obj = InstagramScraper()
    pk = 0
    # store_post_list = StorePost.objects.all().filter(is_updated=True)
    # print(len(store_post_list))

    # for store_post in store_post_list:
    #     store_post.is_updated = False
    #     store_post.save()
    print("changed to not updated --- %s seconds ---" %
          (time.time() - start_time))

    for url in content:
        pk = pk + 1
        print("#{}".format(pk))
        obj.insert_insta(url, created_account, updated_account,
                         deactivated_account, post_error_account, post_0_account)
        # time.sleep(20)

    print("--- %s seconds ---" % (time.time() - start_time))
