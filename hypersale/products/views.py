from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Product, Order, OrderProduct
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
    OrderProductSerializer,
)

class CategoryViewSet(ModelViewSet):
    """
    ViewSet for handling CRUD operations on Category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    """
    ViewSet for handling CRUD operations on Product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'])
    def decrease_stock(self, request, pk=None):
        product = self.get_object()
        quantity = request.data.get("quantity", 0)
        if product.quantity >= int(quantity):
            product.quantity -= int(quantity)
            product.save()
            return Response({"status": "Stock updated", "remaining_stock": product.quantity})
        else:
            return Response({"error": "Not enough stock"}, status=400)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

