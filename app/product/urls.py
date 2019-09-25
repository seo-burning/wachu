from django.urls import path

from product import views

urlpatterns = [
    path('category/<product_category>/',
         views.ProductCategoryListView.as_view()),
    path('search/', views.ProductSearchListView.as_view())
]
