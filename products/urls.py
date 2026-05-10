from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListAPIView.as_view()),
    path('products', views.ProductListAPIView.as_view()),
    path('products/', views.ProductListAPIView.as_view()),
    path('products/<str:pk>', views.ProductDetailAPIView.as_view()),
    path('products/<str:pk>/', views.ProductDetailAPIView.as_view()),
]