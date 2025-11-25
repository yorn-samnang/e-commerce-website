from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from decimal import Decimal

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderDetailSerializer, CreateOrderSerializer
from cart.models import Cart, CartItem


class OrderListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get user's order history"""
        try:
            orders = Order.objects.filter(user=request.user).order_by('-created_at')
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)
        except Exception as e:
            import traceback
            print(f"Error in order list: {str(e)}")
            print(traceback.format_exc())
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        """Create a new order from cart"""
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            # Get user's cart
            try:
                cart = Cart.objects.get(user=request.user)
            except Cart.DoesNotExist:
                return Response(
                    {"error": "Your cart is empty."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if cart has items
            cart_items = CartItem.objects.filter(cart=cart)
            if not cart_items.exists():
                return Response(
                    {"error": "Your cart is empty."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calculate total
            total = Decimal('0.00')
            for item in cart_items:
                total += item.product.price * item.quantity
            
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    address=serializer.validated_data['address'],
                    total=total,
                    status='pending'
                )
                
                # Create order items
                order_items = []
                for cart_item in cart_items:
                    # Check if item is still in stock
                    if cart_item.product.in_stock < cart_item.quantity:
                        transaction.set_rollback(True)
                        return Response(
                            {
                                "error": f"Not enough stock for {cart_item.product.name}. "
                                         f"Available: {cart_item.product.in_stock}"
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # Create order item
                    order_item = OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        name=cart_item.product.name,
                        price=cart_item.product.price,
                        quantity=cart_item.quantity
                    )
                    order_items.append(order_item)
                    
                    # Update stock
                    cart_item.product.in_stock -= cart_item.quantity
                    cart_item.product.save()
                
                # Clear cart
                cart_items.delete()
            
            # Prepare response
            response_data = {
                'order_id': order.id,
                'status': order.status,
                'total': float(order.total),
                'items': [
                    {
                        'product_id': item.product.id,
                        'name': item.name,
                        'quantity': item.quantity,
                        'price': float(item.price)
                    } for item in order_items
                ]
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        """Get detailed information about a specific order"""
        order = get_object_or_404(Order, id=pk, user=request.user)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)
    