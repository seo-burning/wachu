from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from core.models import UserPushToken


# TODO push token 예외 처리와 channel_id 처리
# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(token,
                      body,
                      title,
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
                            # data=data,
                            ttl=ttl,
                            expiration=expiration,
                            priority=priority,
                            sound=sound,
                            badge=badge,
                            # channel_id=channel_id
                            ))
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
