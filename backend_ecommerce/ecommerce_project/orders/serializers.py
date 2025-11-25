from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id')
    name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product_id', 'name', 'quantity', 'price', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.product.image_url:
            return request.build_absolute_uri(obj.product.image_url.url) if request else obj.product.image_url.url
        return None


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='id', read_only=True)
    
    class Meta:
        model = Order
        fields = ['order_id', 'status', 'total', 'created_at']


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    order_id = serializers.IntegerField(source='id', read_only=True)
    
    class Meta:
        model = Order
        fields = ['order_id', 'status', 'address', 'total', 'items', 'created_at']


class CreateOrderSerializer(serializers.Serializer):
    address = serializers.CharField(required=True)