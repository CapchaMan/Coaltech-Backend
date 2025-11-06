from django.urls import path
from .views import VendorRegisterView, VendorLoginView, ProductListCreateView, ProductDetailView

urlpatterns = [
    path('api/register/vendor/', VendorRegisterView.as_view(), name='vendor-register'),
    path('api/login/vendor/', VendorLoginView.as_view(), name='vendor-login'),
    path('api/vendor/products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('api/vendor/products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]
