from django.urls import path

from store import views

urlpatterns = [
    path('stores/', views.StoreView.as_view(), name='store-list'),
    path('list/', views.StoreListView.as_view(), name='store-list-view'),
    path('stores/<store_insta_id>/', views.StorePostView.as_view()),
]
