
from rest_framework import authentication
from allauth.socialaccount.providers.facebook.views \
    import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView, SocialConnectView
from allauth.account.adapter import get_adapter
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import AppleClientToken
from rest_framework import status
import jwt


class FacebookLoginConnect(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter
    authentication_classes = (authentication.TokenAuthentication,)

    def process_login(self):
        print(self.request)
        get_adapter(self.request).login(self.request, self.request.user)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    authentication_classes = (authentication.TokenAuthentication,)


class TemporaryAppleLoginView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request, format=None):
        return Response({})

    def post(self, request, format=None):
        client_token = request.data.__getitem__('client_token')
        try:
            decoded = jwt.decode(client_token, "", verify=False)
            user_unique_id = decoded['sub']
            created_client_token = AppleClientToken.objects.get(
                user_unique_id=user_unique_id)
            data = {"key": created_client_token.user.auth_token.key}
            print(data)
            return Response(data, status=status.HTTP_200_OK)
        except AppleClientToken.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


class TemporaryAppleLoginConnectView(APIView):
    adapter_class = FacebookOAuth2Adapter
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request, format=None):
        user = self.request.user
        client_token = request.data.__getitem__('client_token')
        try:
            decoded = jwt.decode(client_token, "", verify=False)
            user_unique_id = decoded['sub']
            created_client_token, is_exist = AppleClientToken.objects.get_or_create(
                user_unique_id=user_unique_id)
            created_client_token.user = user
            created_client_token.save()
            print(created_client_token.user.auth_token.key)
            data = {"key": created_client_token.user.auth_token.key}
            return Response(data, status=status.HTTP_201_CREATED)
        except AppleClientToken.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
