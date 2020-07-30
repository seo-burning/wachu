
from rest_framework import authentication
from allauth.socialaccount.providers.facebook.views \
    import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView, SocialConnectView
from allauth.account.adapter import get_adapter
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import AppleClientToken


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
            created_client_token = AppleClientToken.objects.get(
                client_token=client_token)
            print(created_client_token)
            return Response({"is_exist": True})
        except AppleClientToken.DoesNotExist:
            return Response({"is_exist": 400})


class TemporaryAppleLoginConnectView(APIView):
    adapter_class = FacebookOAuth2Adapter
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request, format=None):
        user = self.request
        client_token = request.data.__getitem__('client_token')
        try:
            created_client_token, is_exist = AppleClientToken.objects.get_or_create(
                client_token=client_token, user=user)
            print(created_client_token)
            return Response({"is_exist": True})
        except AppleClientToken.DoesNotExist:
            return Response({"is_exist": 400})
