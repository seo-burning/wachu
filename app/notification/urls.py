from django.urls import path
from . import views

app_name = 'notification'

# TODO url pattern 통일 필요.
urlpatterns = [
    path('me/', views.UserNotificationListView.as_view(), name='user_notification_list'),
    path('update/<int:pk>', views.UserNotificationUpdateView.as_view(), name='user_notification_update')

]
