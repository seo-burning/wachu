from django.urls import path

from publish import views

urlpatterns = [
    path('post-group/', views.MainPagePublishView.as_view()),
]
