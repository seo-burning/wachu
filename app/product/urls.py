from django.urls import path

from product import views

urlpatterns = [
    path('sliding-banner-section/', views.SlidingBannerSectionView.as_view()),
    path('main-section/', views.MainSectionView.as_view())
]
