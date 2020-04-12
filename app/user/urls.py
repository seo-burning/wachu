from django.urls import path
from django.conf.urls import include
from user import views


app_name = 'user'

urlpatterns = [
    path('rest_auth/register/', include('rest_auth.registration.urls')),
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('push_token/', views.UserPushTokenListView.as_view(),
         name='push_token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('me/basic/', views.UserBasicInfoUpdateView.as_view(),
         name='basic_info_update'),
    path('me/additional/', views.UserAdditionalInfoUpdateView.as_view(),
         name='additional_info_update'),
    path('me/name/', views.UserNameUpdateView.as_view(),
         name='name_update'),
    path('me/push_token/', views.CreatUserPushToken.as_view(),
         name='push_token'),
    path('facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('facebook/connect/', views.FacebookLoginConnect.as_view(),
         name='fb_login_connect'),

    path('favorite/', views.FavoriteListView.as_view(),
         name='favorite'),
    path('favorite/product/', views.FavoriteProductListView.as_view()),
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
