from django.urls import path

from store import views

app_name = 'store'

urlpatterns = [
    path('stores/', views.StoreView.as_view(), name='store-list'),
    path('stores/<store_insta_id>/', views.StorePostView.as_view()),
]
