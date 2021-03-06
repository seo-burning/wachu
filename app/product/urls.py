from django.urls import path

from product import views

urlpatterns = [
    path('category/<product_category>/',
         views.ProductCategoryListView.as_view()),
    path('search/', views.ProductSearchListView.as_view()),
    path('get-rating/<int:pk>/', views.ProductRatingView.as_view()),
    path('category-list/', views.CategoryListView.as_view()),
    path('product/<int:pk>', views.ProductDetailView.as_view())
]
