from django.urls import path
from order import views

app_name = 'order'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('create/status/', views.OrderStatusLogCreateView.as_view(), name='order_status_log_create'),
    path('user/', views.OrderSummaryView.as_view(), name='order_summary'),
    path('update/<int:pk>/', views.OrderRetrieveUpdateView.as_view(),
         name='order_retrieve_update'),
    path('coupon/', views.CouponListView.as_view(), name='coupon_list'),
    path('coupon/validate/', views.CouponValidateView.as_view(), name='validate_coupon'),
    path('delivery-status/<str:slug>/', views.DeliveryStatusView.as_view(), name='delivery_status'),
    path('<str:status>/', views.OrderListView.as_view(), name='order_list'),
]
