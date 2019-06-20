from django.urls import path

from pick import views

urlpatterns = [
    path('chu-pick-set/', views.ChuPickSetView.as_view()),
]
