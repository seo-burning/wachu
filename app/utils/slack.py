from slacker import Slacker
# from slack import WebClient
# from slack.errors import SlackApiError
import os

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')


def slack_notify(text=None, channel='#5_db_crawler', attachments=None):
    token = SLACK_TOKEN
    slack = Slacker(token)
    slack.chat.post_message(channel=channel, text=text, attachments=attachments)


# def slack_upload_file(file_path):
#     client = WebClient(token=os.environ['SLACK_TOKEN'])
#     try:
#         response = client.files_upload(
#             channels='#5_db_crawler',
#             file=file_path)
#         assert response["file"]  # the uploaded file
#     except SlackApiError as e:
#         # You will get a SlackApiError if "ok" is False
#         assert e.response["ok"] is False
#         assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
#         print(f"Got an error: {e.response['error']}")


if __name__ == '__main__':
    slack_notify('new order created', channel='#7_order')
