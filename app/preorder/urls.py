from django.urls import path
from preorder import views

urlpatterns = [
    path('', views.PreorderListView.as_view()),
    path('<int:pk>/', views.PreorderProductView.as_view())
]
