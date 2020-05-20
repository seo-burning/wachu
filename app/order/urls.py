from django.urls import path
from order import views

app_name = 'order'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('user/', views.OrderSummaryView.as_view(), name='order_summary'),
    path('update/<int:pk>/', views.OrderRetrieveUpdateView.as_view(),
         name='order_retrieve_update'),
    path('<str:status>/', views.OrderListView.as_view(), name='order_list'),
]
