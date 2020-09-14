from django.urls import path

from publish import views

urlpatterns = [
    path('main-page/', views.MainPagePublishView.as_view()),
    path('main-page/tags/', views.ProductTagGroupListView.as_view()),
    path('main-page/banner/', views.BannerPublishView.as_view()),
    path('magazine/', views.MagazinePublishView.as_view()),
    path('exhibition/<int:pk>/', views.ProductGroupDetailView.as_view()),

]
