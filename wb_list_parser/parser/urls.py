from django.urls import path
from .views import (
    ProductListAPIView, 
    ProductCategoryListAPIView, 
    ProductsParserAPIView, 
    ParserHistoryListAPIView, 
    ProductRetrieveAPIView
    )


urlpatterns = [
    path("products/",   ProductListAPIView.as_view(), name="products-list"),
    path("products/<int:pk>/", ProductRetrieveAPIView.as_view(), name="product-info"),
    path("categories/", ProductCategoryListAPIView.as_view(), name="categories-list"),
    
    path("parse-products/", ProductsParserAPIView.as_view(), name="products-parser"),
    path("parser-history/", ParserHistoryListAPIView.as_view(), name="parser-history"),
]
