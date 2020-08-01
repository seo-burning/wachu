from rest_framework import generics, authentication, permissions
from .models import UserNotification
from .serializers import UserNotificationSerializer, UserNotificationReadUpdateSerializer


class UserNotificationUpdateView(generics.UpdateAPIView):
    serializer_class = UserNotificationReadUpdateSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = UserNotification.objects.all()


class UserNotificationListView(generics.ListAPIView):
    serializer_class = UserNotificationSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = UserNotification.objects.filter(user=user)
        return queryset
