from django.urls import path
from . import views

app_name = 'advertisement'

urlpatterns = [
    path('search-recommend/store/',
         views.StoreRecommendKeywordListViewAPI.as_view(),
         name='store-search-recommend'),
    path('search-recommend/product/',
         views.ProductRecommendKeywordListViewAPI.as_view(),
         name='product-search-recommend'),
]
