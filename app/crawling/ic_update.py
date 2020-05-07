
from ic_video import video_file_update_with_video_source
from product.models import Product, ProductCategory, ProductSubCategory, ProductColor, ProductStyle
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

PROJECT_ROOT = os.getcwd()
sys.path.append(os.path.dirname(PROJECT_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.prod")
django.setup()

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

    def get_content_from_post_page_single(self, request_url):
        results = []
        try:
            response = self.__request_url(request_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        except Exception as e:
            print("Failed in Posts {} {}".format(request_url, e))
        return metrics

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
                print('502 Error, sever issue')
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
            else:
                if obj_post.post_type == 'MP':
                    for obj_old_post in obj_post.post_image_set.all():
                        obj_old_post.delete()
                    post_images = self.get_content_from_post_page(post_url)
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
                        obj_image.save()
                elif obj_post.post_type == 'V':
                    post_video = self.get_video_from_post_page(
                        post_url)
                    print('V')
                    video_file_update_with_video_source(
                        obj_post, post_video['video_url'], post_video['thumbnail_src'])
                    obj_post.view_count = post_video['video_view_count']
                    obj_post.save()

        except Exception as e:
            print(e)


def deactive_post_by_store(obj_store):
    obj_list = StorePost.objects.all().filter(
        is_active=True).filter(store=obj_store)
    print(obj_store, obj_list.count())
    for i, obj_post in enumerate(obj_list):
        obj_post.is_active = False
        obj_post.save()


def auto_fill_product():
    store_obj = Store.objects.all().get(insta_id='20decemberjeans')
    store_post_list = StorePost.objects.all().filter(
        store=store_obj).filter(product=None, is_product='P')
    post_category = ProductCategory.objects.all().get(name='pants')
    sub = ProductSubCategory.objects.all().get(name='jeans')
    color_p = ProductColor.objects.all().get(name='black')
    style = ProductStyle.objects.all().get(name='simple')

    print(store_post_list.count())
    print(sub, style, post_category)
    for store_post_obj in store_post_list:
        product_obj, is_created = Product.objects.get_or_create(
            store=store_obj, post=store_post_obj, category=post_category, sub_category=sub, style=style)
        product_obj.color.add(color_p)
        product_obj.save()
    # print("--- %s seconds ---" % (time.time() - start_time))


# 자주 포스트를 지우는 계정 리스트 확인.

def re_update_mp_post_with_video(obj_post):
    obj = InstagramScraper()
    post_image_obj_list = PostImage.objects.all().filter(
        store_post=obj_post, post_image_type='V')
    if post_image_obj_list.count() > 0:
        print("------------------" + str(obj_post.pk))
        obj.re_update_everything(obj_post)


def all_store_re_update_mp_post_with_video():
    store_list = Store.objects.all().filter(
        is_active=True).order_by('current_ranking')
    print(store_list.count())
    import multiprocessing as mp
    for store_obj in store_list:
        post_list = StorePost.objects.all().filter(
            is_active=True, store=store_obj, post_type='MP')
        print(store_obj.insta_id, post_list.count())
        for post_obj in post_list:
            re_update_mp_post_with_video(post_obj)
        # for obj_post in post_list:
        #     post_image_obj_list = PostImage.objects.all().filter(
        #         store_post=obj_post, post_image_type='V')
        #     if post_image_obj_list.count() > 0:
        #         print(obj_post.pk)
        #         obj.re_update_everything(obj_post)


def re_update_post_with_video():
    obj = InstagramScraper()
    store_list = Store.objects.all().filter(
        is_active=True).order_by('current_ranking')
    for store_obj in store_list:
        post_list = StorePost.objects.all().filter(
            is_active=True, store=store_obj, post_type='V')
        print(store_obj.insta_id, post_list.count())
        for post_obj in post_list:
            print(post_obj.pk)
            obj.re_update_everything(post_obj)


if __name__ == '__main__':
    start_time = time.time()

    import multiprocessing as mp
    from functools import partial
    # pool = mp.Pool(processes=6)
    all_store_re_update_mp_post_with_video()


def _update_insta_post_to_product(product_obj):
    post_obj = product_obj.post
    if post_obj == None:
        print('delete')
        product_obj.delete()
        return None
    product_obj.description = post_obj.post_description
    product_obj.product_link = post_obj.post_url
    product_obj.product_source = 'INSTAGRAM'
    product_obj.is_active = True
    thumb_image_pk = product_obj.thumb_image_pk
    post_image_set = post_obj.post_image_set.all()
    image_count = post_image_set.count()
    print(image_count, thumb_image_pk, post_obj.post_type)
    if post_obj.post_type == 'V':
        product_obj.video_source = post_obj.video_source
        product_obj.product_thumbnail_image = post_obj.post_thumb_image
        product_image_obj, is_created = ProductImage.objects.get_or_create(source_thumb=post_obj.post_thumb_image,
                                                                           post_image_type='V',
                                                                           source=post_obj.video_source, product=product_obj)

    else:
        product_obj.product_thumbnail_image = post_image_set[image_count - thumb_image_pk].source_thumb
        product_obj.product_image_type = post_obj.post_type
        product_obj.video_source = post_obj.video_source
        for i, post_image in enumerate(post_image_set):
            product_image_obj, is_created = ProductImage.objects.get_or_create(source_thumb=post_image.source_thumb,
                                                                               post_image_type=post_image.post_image_type,
                                                                               source=post_image.source, product=product_obj)
    product_obj.save()


def update_insta_post_to_product():
    product_list = Product.objects.filter(product_source='')
    for product_obj in product_list:
        _update_insta_post_to_product(product_obj)
    print(len(product_list))
