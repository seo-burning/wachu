from django.urls import path
from order import views

app_name = 'order'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    # path('create/product/', views.OrderCreateView.as_view(), name='order_create_product')
]
