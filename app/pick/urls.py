from django.urls import path

from pick import views

urlpatterns = [
    path('pick-set/', views.PickSetView.as_view()),
    path('list/', views.RandomPickListView.as_view()),
    path('pick-ab/create/', views.PickABResultCreateView.as_view()),
    path('me/', views.MyPickListView.as_view())

]
