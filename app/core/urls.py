from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('notice/', views.NoticeListViewAPI.as_view(), name='notice-list')
]
