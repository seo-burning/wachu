from django.urls import path

from pick import views

urlpatterns = [
    path('pick-set/', views.PickSetView.as_view()),
]
