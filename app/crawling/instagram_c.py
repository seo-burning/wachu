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
from store_point_logic import calculate_post_point
import multiprocessing as mp
from functools import partial
from time import sleep
import random
from django.db.models import Q

from helper.instagram_helper import resize_thumbnail_by_store
from ic_video import video_file_update_with_video_source, video_file_update_with_video_source_post_product_image
# # # from utils.slack import slack_notify, slack_upload_file

import os_setup

from store.models import Store, StorePost, StoreRanking, PostImage


_user_agents = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxy_list = soup.find('tbody')
    proxies = set()
    for rows in proxy_list.find_all('tr')[0:20]:
        if rows.find_all('td')[6].text == 'yes':
            proxies.add(rows.find_all('td')[0].text +
                        ':'+rows.find_all('td')[1].text)
    return proxies


# dateInfo = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime('%Y-%m-%d')


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
            headers = self.__random_agent()
            proxies = self.__random_proxies()
            response = requests.get(url, headers={'User-Agent': headers, 'Referer': 'https://www.instagram.com'},
                                    proxies={'http': None, 'https':  None})
            print(proxies)
            response.raise_for_status()
        except requests.HTTPError as e:
            print(e)
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response.text

    @staticmethod
    def extract_json_data(html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = str(body.find('script'))
        raw_string = script_tag.replace('<script type="text/javascript">', '').replace('</script>', '').replace(
            'window._sharedData =', '').replace(';', '').strip()
        return json.loads(raw_string)

    def profile_page_metrics(self, profile_url):
        results = {}
    # try:
        response = self.__request_url(profile_url)
        json_data = self.extract_json_data(response)
        metrics = json_data['entry_data']
        print(metrics)
        metrics = metrics['ProfilePage'][0]['graphql']['user']
        print('execute profile')
    # except Exception as e:
    #     print(e)
    #     print('error occured')
    #     slack_notify("Failed in Get Posts {} {}".format(profile_url, e))
    #     pass
    # else:
        print(len(metrics.items()))
        for key, value in metrics.items():
            if value and isinstance(value, dict):
                print(key)
                if 'count' in value:
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
            # slack_notify("Failed in Get Posts {} {}".format(profile_url, e))
            print(e)
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
            # slack_notify("Failed in Get Single Posts {} {}".format(request_url, e))
            print('Error occured when get specific post data')
            pass
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
            # slack_notify("Failed in Get Posts'  video{} {}".format(request_url, e))
            pass
        return metrics

    def update_profile(self, url):
        print(url)
        results = self.profile_page_metrics(url)
        if results['username']:
            obj_store, is_created = Store.objects.get_or_create(
                insta_id=results['username'])
            obj_store.is_updated = True
            name = results['username']
            if 'full_name' in results.keys():
                name = results['full_name']
            obj_store.name = name
            obj_store.follower = results['edge_followed_by']
            obj_store.following = results['edge_follow']
            obj_store.post_num = results['edge_owner_to_timeline_media']
            description = ''
            if 'biography' in results.keys():
                description = results['biography']
            obj_store.description = description
            obj_store.profile_image = results['profile_pic_url_hd']
            obj_store.save()

    def insert_insta(self, url):
        results = {}
        results = self.profile_page_metrics(url)
        # sleep(2+random.random()*15)
        result_post = []
        result_post = self.profile_page_recent_posts(url)
        # sleep(2+random.random()*15)

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
            new_post = 0
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
                            new_post = new_post + 1
                            if post['__typename'] == 'GraphSidecar':
                                obj_post.post_type = 'MP'
                                post_images = self.get_content_from_post_page(
                                    post_url)
                                # sleep(2+random.random()*15)
                                obj_post.post_thumb_image = post_images[0]['display_resources'][0]['src']
                                obj_post.save()
                                for image in post_images:
                                    obj_image, image_is_created = PostImage.objects.get_or_create(
                                        source=image['display_url'],
                                        source_thumb=image['display_resources'][0]['src'],
                                        store_post=obj_post,
                                        post_image_type='P')
                                    if image['__typename'] == 'GraphVideo':
                                        obj_image.post_image_type = 'V'
                                        obj_image.source = image['video_url']
                                        obj_image.source_thumb = image['display_resources'][0]['src']
                                        video_file_update_with_video_source_post_product_image(
                                            obj_image, image['video_url'], image['display_resources'][0]['src'])
                                        obj_image.save()
                            elif post['__typename'] == 'GraphVideo':
                                obj_post.post_type = 'V'
                                post_video = self.get_video_from_post_page(
                                    post_url)
                                # sleep(2+random.random()*15)
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
                        print(e, end='')
                        pass

            else:
                print("Fail to Find post. Account may be Private")
            obj_store.is_new_post = is_new_post
            obj_store.save()
            resize_thumbnail_by_store(obj_store)

            if (is_created):
                print("C - {} (id:{} / {} post saved.)".format(username,
                                                               obj_store.id, post_saved))
            elif (is_created == False):
                print("U - {} (id:{} / {} post saved.)".format(username,
                                                               obj_store.id, post_saved))
            return new_post
            time.sleep(5)


def update_user_profile_image():
    obj = InstagramScraper()
    store_list = Store.objects.exclude(store_type='DS')[120:]
    content = ['https://www.instagram.com/' +
               x.insta_id + '/' for x in store_list]
    print('updates', len(content))
    for url in list(content):
        obj.update_profile(url)


def update_instagram():
    pk = 0
    dateInfo = datetime.datetime.now().strftime('%Y-%m-%d')
    file_path = './instagram_result.txt'
    store_list = Store.objects.all().filter(Q(
        store_type='IF(P)') | Q(
        store_type='IF')).order_by('current_ranking')
    content = ['https://www.instagram.com/' +
               x.insta_id + '/' for x in store_list]
    obj = InstagramScraper()
    total_new_post = 0
    print(len(content))
    with open(file_path, "w") as f:
        for url in list(content):
            pk = pk + 1
            new_post = obj.insert_insta(url)
            if new_post == None:
                new_post = 0
            total_new_post = total_new_post + new_post
            result_text = "{} save new post : #{} // total : #{}".format(url, new_post, total_new_post)
            f.writelines(result_text)
    # slack_notify(">updated store : {} total created post : {}".format(str(pk), str(total_new_post)))
    # slack_upload_file(file_path)
    os.remove(file_path)


if __name__ == '__main__':
    print('start scrapying')

    start_time = time.time()

    dateInfo = input('date info input : ')
    if dateInfo:
        print(dateInfo)
    else:
        dateInfo = datetime.datetime.now().strftime('%Y-%m-%d')
        print(dateInfo)
    store_list = Store.objects.all().filter(Q(
        store_type='IF(P)')).order_by('current_ranking')
    print("total active store: #{}".format(len(store_list)))
    all_store_ranking_objs_for_today = StoreRanking.objects.filter(
        date=dateInfo).filter(store__is_active=True)
    print("already exist data: #{}".format(
        len(all_store_ranking_objs_for_today)))
    start_num = len(all_store_ranking_objs_for_today)
    print("start crwaling from: #{}".format(start_num))

    store_list = store_list[start_num:]
    content = ['https://www.instagram.com/' +
               x.insta_id + '/' for x in store_list]
    obj = InstagramScraper()
    pk = start_num
    print("changed to not updated --- %s seconds ---" %
          (time.time() - start_time))

    total_new_post = 0
    for url in list(content):
        pk = pk + 1
        print("ranking #{}".format(pk))
        new_post = obj.insert_insta(url)
        if new_post == None:
            new_post = 0
        total_new_post = total_new_post + new_post
        print("save new post : #{} // total : #{}".format(new_post, total_new_post))
        break

    print(total_new_post)
    print("--- %s seconds ---" % (time.time() - start_time))
