from slacker import Slacker
import os

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')


def slack_notify(text=None, channel='#5_db_crawler', attachments=None):
    token = SLACK_TOKEN
    slack = Slacker(token)
    slack.chat.post_message(channel=channel, text=text, attachments=attachments)


if __name__ == '__main__':
    created = ['abc', 'dad', 'adfa']
    slack_notify('test message' + str(len(created)))
    slack_notify('jemclothes')
    for created_obj in created:
        slack_notify(created_obj)
