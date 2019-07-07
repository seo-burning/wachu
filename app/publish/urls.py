from django.urls import path

from publish import views

urlpatterns = [
    path('main-page/', views.MainPagePublishView.as_view()),
]
