from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from core.models import UserPushToken
from .models import UserNotification, PushNotification
from datetime import datetime


# TODO push token 예외 처리와 channel_id 처리
# 일반적으로는 특정 parameter를 가지고, 특정 route로 네비게이션 하는 것. dict => route / params (또다른 dictionary)
# TODO push token 특정 위치로 날아가는거 처리
# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.

# class PushClientWithRetry(PushClient):
#     def _publish_internal(self, push_messages):


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
    token_valid = PushClient().is_exponent_push_token(token.push_token)
    if (token_valid):
        try:
            response = PushClient().publish(
                PushMessage(to=token.push_token,
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
        # Category & display_in_forground
        except PushServerError as exc:
            # Encountered some likely formatting/validation error.
            print('PushServerError')
            print(exc)
            raise
        except (ConnectionError, HTTPError) as exc:
            # Encountered some Connection or HTTP error - retry a few times in
            # case it is transient.
            print('ConnectionError or HTTPError')
            print(exc)
            raise
        try:
            # We got a response back, but we don't know whether it's an error yet.
            # This call raises errors so we can handle them with normal exception
            # flows.
            response.validate_response()
        except DeviceNotRegisteredError:
            # Mark the push token as inactive
            print('Device is not Registered. Make it deactivated')
            UserPushToken.objects.filter(token=token).update(is_active=False)
        except PushResponseError as exc:
            # Encountered some other per-notification error.
            print(exc)
            pass


def send_multiple_push_message(token_list,
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
    push_message_list = []
    for token in token_list:
        token_valid = PushClient().is_exponent_push_token(token.push_token)
        if (token_valid):
            push_message_list.append(PushMessage(to=token.push_token,
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
            print(',', end='')
    try:
        response = PushClient().publish_multiple(push_message_list)
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
        # UserPushToken.objects.filter(token=token).update(active=False)
        pass
    except PushResponseError as exc:
        # Encountered some other per-notification error.
        print(exc)
        pass


def send_test_notification(body, title, data=None):
    user_push_token_list = []
    user_push_token_1 = UserPushToken.objects.get(push_token='ExponentPushToken[_Vn_lOLvJCT0gVcBisvTLk]')
    user_push_token_2 = UserPushToken.objects.get(push_token='ExponentPushToken[TTFcgxLxhAdB8TiU5UnRQA]')
    user_push_token_list.append(user_push_token_1)
    user_push_token_list.append(user_push_token_2)
    send_multiple_push_message(user_push_token_list, body, title, data)
    notification_obj, is_created = PushNotification.objects.get_or_create(title=title, body=body, data=data)
    print(is_created)
    for push_token_obj in user_push_token_list:
        UserNotification.objects.create(title=notification_obj.title,
                                        body=notification_obj.body,
                                        data=notification_obj.data,
                                        publish_date=datetime.now(),
                                        notification=notification_obj,
                                        user=push_token_obj.user,
                                        push_token=push_token_obj
                                        )


def send_multiple_push_message_to_all(body, title, data=None):
    user_push_token_list = UserPushToken.objects.filter(is_active=True)
    print("total push estimate : {}".format(len(user_push_token_list)))
    # user_push_token_list = []
    # user_push_token = UserPushToken.objects.get(push_token='ExponentPushToken[_Vn_lOLvJCT0gVcBisvTLk]')
    # for i in range(0, 150):
    #     user_push_token_list.append(user_push_token)
    i = 50
    while True:
        if i + 50 > len(user_push_token_list):
            try:
                send_multiple_push_message(user_push_token_list[i:], body, title, data)
                print("push success from {} to end".format(i))
            except Exception:
                print("error occured from {} to end".format(i))
            break
        else:
            try:
                send_multiple_push_message(user_push_token_list[i:i + 50], body, title, data)
                print("push success from {} to {}".format(i, i+50))
            except Exception:
                print("error occured from {} to {}".format(i, i+50))
            i = i + 50
