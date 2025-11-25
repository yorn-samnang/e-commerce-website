# cart/views.py

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from products.models import Product
from .models import Cart, CartItem
from .serializers import CartItemSerializer, AddToCartSerializer, UpdateCartItemSerializer


class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get user's cart items"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Add item to cart"""
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            
            product = get_object_or_404(Product, id=product_id)
            
            # Check if quantity is available
            if product.in_stock < quantity:
                return Response(
                    {"error": f"Only {product.in_stock} items available in stock."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return Response({"message": "Added to cart"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, product_id):
        """Update cart item quantity"""
        serializer = UpdateCartItemSerializer(data=request.data)
        if serializer.is_valid():
            quantity = serializer.validated_data['quantity']
            
            cart = get_object_or_404(Cart, user=request.user)
            product = get_object_or_404(Product, id=product_id)
            cart_item = get_object_or_404(CartItem, cart=cart, product=product)
            
            # Check if quantity is available
            if product.in_stock < quantity:
                return Response(
                    {"error": f"Only {product.in_stock} items available in stock."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            cart_item.quantity = quantity
            cart_item.save()
            
            return Response({"message": "Cart updated"})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, product_id):
        """Remove item from cart"""
        cart = get_object_or_404(Cart, user=request.user)
        product = get_object_or_404(Product, id=product_id)
        
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
            return Response({"message": "Item removed from cart"})
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)