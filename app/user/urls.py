from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('favorite/', views.FavoriteListView.as_view(),
         name='favorite'),
    path('favorite/store/create/', views.FavoriteStoreCreateView.as_view(),
         name='favorite_store_create'),
    path('favorite/store/<int:pk>/',
         views.FavoriteStoreView.as_view(),
         name='favorite_store_delete'),
    path('favorite/post/<int:pk>/',
         views.FavoritePostView.as_view(),
         name='favorite_post_delete'),
    path('favorite/post/create',
         views.FavoritePostCreateView.as_view(),
         name='favorite_post_create'),
]
