# cart/urls.py
from django.urls import path
from .views import CartView, CartItemView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),  # This will be /api/cart/
    path('<int:product_id>/', CartItemView.as_view(), name='cart_item'),  # This will be /api/cart/<product_id>/
]