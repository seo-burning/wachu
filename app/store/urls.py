from django.urls import path, include
from rest_framework.routers import DefaultRouter

from store import views

router = DefaultRouter()
router.register('stores', views.StoreViewSet)

app_name = 'store'

urlpatterns = [
    path('', include(router.urls)),
    path('stores/<store_insta_id>/', views.StorePostView.as_view())
]
