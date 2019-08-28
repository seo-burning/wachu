from django.urls import path

from publish import views

urlpatterns = [
    path('main-page/', views.MainPagePublishView.as_view()),
    path('main-page/banner/', views.BannerPublishView.as_view()),
    path('test/', views.TestPostSerializer.as_view())
]
