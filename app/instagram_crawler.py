
import sys
import os
import django
import json
import requests
from bs4 import BeautifulSoup
from random import choice
from time import sleep
import pymsteams  # https://pypi.org/project/pymsteams/
import datetime


PROJECT_ROOT = os.getcwd()
sys.path.append(os.path.dirname(PROJECT_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.prod")
django.setup()
from store.models import Store, StorePost

_user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
]

created_account = []
updated_account = []
deactivated_account = []
post_error_account = []


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
        except requests.HTTPError:
            deactivated_account.append(url)
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
            print("Failed {}".format(profile_url))
            deactivated_account.append(profile_url)
            pass
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node)
        return results

    def insert_insta(self, url):
        results = {}
        results = self.profile_page_metrics(url)
        result_post = []
        result_post = self.profile_page_recent_posts(url)

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
            obj_store.save()

            post_saved = 0
            if len(result_post) > 0:
                for post in result_post:
                    post_url = ''
                    post_like = 0
                    post_commnet = 0
                    post_description = ''
                    post_taken_at_timestamp = 0
                    try:
                        if 'display_url' in post:
                            post_url = post['display_url']
                            post_like = post['edge_liked_by']['count']
                        if 'edge_media_to_comment' in post:
                            post_comment = post['edge_media_to_comment']['count']
                        if 'taken_at_timestamp' in post:
                            post_taken_at_timestamp = post['taken_at_timestamp']
                        if 'edge_media_to_caption' in post:
                            try:
                                post_description = post['edge_media_to_caption']['edges'][0]['node']['text']
                            except:
                                pass
                        obj, is_created = StorePost.objects.get_or_create(
                            post_image=post_url, store=obj_store)
                        obj.post_like = post_like
                        obj.post_description = post_description
                        obj.post_comment = post_comment
                        obj.post_taken_at_timestamp = post_taken_at_timestamp
                        obj.save()
                        post_saved = post_saved + 1
                    except IndexError as e:
                        print('E', end='')
                        post_error_account.append(obj_store.insta_url)
                        pass

            if (is_created):
                created_account.append(obj_store.insta_url)
                print("C - {} (id:{} / {} post saved.)".format(username,
                                                               obj_store.id, post_saved))
            elif (is_created == False):
                updated_account.append(obj_store.insta_url)
                print("U - {} (id:{} / {} post saved.)".format(username,
                                                               obj_store.id, post_saved))


def report_to_teams(url, created_account_list, updated_account_list, deactivated_account_list, post_error_account_list):
    ca_len = len(created_account_list)
    ua_len = len(updated_account_list)
    da_len = len(deactivated_account_list)
    pe_len = len(post_error_account_list)

    myTeamsMessage = pymsteams.connectorcard(url)
    updatedAt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    myTeamsMessage.title("Crawling Result @{}".format(updatedAt))
    myTeamsMessage.text("Crawling Result @{}".format(updatedAt))
    myTeamsMessage.addLinkButton("To AdminSite", "https://www.naver.com/")

    SummarySection = pymsteams.cardsection()
    SummarySection.addFact("Created", ca_len)
    SummarySection.addFact("Updated", ua_len)
    SummarySection.addFact("Deactivated", da_len)
    SummarySection.addFact("Post Error", pe_len)
    # Section Title

    CreatedListSection = pymsteams.cardsection()
    CreatedListSection.activityTitle("Created List {}".format(ca_len))
    section_text = ''
    for item in created_account_list:
        section_text = section_text + \
            "<p><a href='{}'>{}</a></p>".format(
                item, item)
    CreatedListSection.text(section_text)

    DeactivatedListSection = pymsteams.cardsection()
    DeactivatedListSection.activityTitle("Deactivated List {}".format(da_len))
    section_text = ''
    for item in deactivated_account_list:
        section_text = section_text + \
            "<p><a href='{}'>{}</a></p>".format(
                item, item)
    DeactivatedListSection.text(section_text)

    PostErrorListSection = pymsteams.cardsection()
    PostErrorListSection.activityTitle("PostError List {}".format(pe_len))
    section_text = ''
    for item in post_error_account_list:
        section_text = section_text + \
            "<p><a href='{}'>{}</a></p>".format(
                item, item)
    PostErrorListSection.text(section_text)

    myTeamsMessage.addSection(SummarySection)
    myTeamsMessage.addSection(CreatedListSection)
    myTeamsMessage.addSection(DeactivatedListSection)
    myTeamsMessage.addSection(PostErrorListSection)

    myTeamsMessage.send()


if __name__ == '__main__':

    with open('crawling/account_list.txt', 'r') as f:
        content = f.readlines()

    content = [x.strip() for x in content]

    obj = InstagramScraper()
    for account in content:
        acc = 'https://www.instagram.com/' + account + '/'
        obj.insert_insta(acc)
        sleep(1)
    deactivated_account_list = set(deactivated_account)
    post_error_account_list = set(post_error_account)
    updated_account_list = set(updated_account)
    created_account_list = set(created_account)
    url = 'https://outlook.office.com/webhook/d9d7a72c-a2ed-408a-af8c-11d5fe4f644c@91737814-ef77-47df-924e-004375937240/IncomingWebhook/b8b0ed239e544929b960847316a1d6c7/692ad803-8ead-405e-a95e-ca10cff195db'
    print("{} created, {} updated, {} failed in post, {} deactivated(failed)".format(len(created_account_list),
                                                                                     len(
                                                                                         updated_account_list),
                                                                                     len(
                                                                                         post_error_account_list),
                                                                                     len(deactivated_account_list)))

    report_to_teams(url, created_account_list, updated_account_list,
                    deactivated_account_list, post_error_account_list)
    with open('crawling/crawling_result.txt', 'wt') as f:
        f.write("{} created, {} updated, {} failed in post, {} deactivated(failed)\n".format(len(created_account_list),
                                                                                             len(
                                                                                                 updated_account_list),
                                                                                             len(
                                                                                                 post_error_account_list),
                                                                                             len(deactivated_account_list)))
        f.write('\ncreated_account_list \n')
        created_account_list = map(lambda x: x + '\n', created_account_list)
        f.writelines(created_account_list)
        f.write('\ndeactivated_account_list \n')
        deactivated_account_list = map(
            lambda x: x + '\n', deactivated_account_list)
        f.writelines(deactivated_account_list)
        f.write('\nfailed in post \n')
        post_error_account_list = map(
            lambda x: x + '\n', post_error_account_list)
        f.writelines(post_error_account_list)
