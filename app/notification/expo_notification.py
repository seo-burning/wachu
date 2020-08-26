from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from core.models import UserPushToken


# TODO push token 예외 처리와 channel_id 처리
# 일반적으로는 특정 parameter를 가지고, 특정 route로 네비게이션 하는 것. dict => route / params (또다른 dictionary)
# TODO push token 특정 위치로 날아가는거 처리
# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(token,
                      body='',
                      title='',
                      data=None,
                      ttl=None,
                      expiration=None,
                      priority='default',
                      subtitle=None,
                      sound='default',
                      badge=1,
                      channel_id=None,
                      ):
    token_valid = PushClient().is_exponent_push_token(token)
    print(token_valid)
    if (token_valid):
        try:
            response = PushClient().publish(
                PushMessage(to=token,
                            body=body,
                            title=title,
                            data=data,
                            ttl=ttl,
                            expiration=expiration,
                            priority=priority,
                            sound=sound,
                            badge=badge,
                            channel_id=channel_id
                            ))
            return True
        # Category & display_in_forground
        except PushServerError as exc:
            # Encountered some likely formatting/validation error.
            print(exc)
            pass
        except (ConnectionError, HTTPError) as exc:
            # Encountered some Connection or HTTP error - retry a few times in
            # case it is transient.
            print(exc)
            pass
        try:
            # We got a response back, but we don't know whether it's an error yet.
            # This call raises errors so we can handle them with normal exception
            # flows.
            response.validate_response()
        except DeviceNotRegisteredError:
            # Mark the push token as inactive
            UserPushToken.objects.filter(token=token).update(active=False)
        except PushResponseError as exc:
            # Encountered some other per-notification error.
            print(exc)
            pass


# from notification.expo_notification import send_push_message
# token = "ExponentPushToken[4lj2vJFckW5W3AFWJgxXT-]"
# send_push_message(token, 'test', 'test_123',data={'route':'store','params':{}})
# if __name__ == '__main__':
#     user_push_tokens = UserPushToken.objects.all()
#     title = input('title : ')
#     body = input('body : ')
    # pool = mp.Pool(processes=64)
    # pool.map()
# for token in user_push_tokens:
#     try:
#         expo_notification.send_push_message(token.push_token, body, title)
#         print('.', end='')
#     except:
#         print('e', end='')
#         pass
