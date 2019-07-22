from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('favorite/', views.FavoriteStoreListView.as_view(),
         name='favorite'),
    path('favorite/store/<str:pk>/delete/',
         views.FavoriteStoreObjectView.as_view(),
         name='favorite_store_delete'),
    path('favorite/store/create/', views.FavoriteStoreCreateView.as_view(),
         name='favorite_store_create'),

]
