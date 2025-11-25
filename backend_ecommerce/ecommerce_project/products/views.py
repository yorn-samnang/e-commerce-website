from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer, ProductCreateUpdateSerializer
from .permissions import IsAdminOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        
        # Handle search parameter
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search)
            )
        
        # Handle category parameter
        category = self.request.query_params.get('category', None)
        if category:
            # In a real app, you might have a category model or field
            # This is a placeholder for demonstration
            queryset = queryset.filter(name__icontains=category)
            
        return queryset