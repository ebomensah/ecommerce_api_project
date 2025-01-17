from django.shortcuts import get_object_or_404
from django_filters.filters import OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Product, Order, Review, Wishlist, Discount
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
    ReviewSerializer,
    WishlistSerializer,
    DiscountSerializer
)
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['name', 'description']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name = "name", lookup_expr='icontains')
    category = filters.CharFilter(field_name="category__name", lookup_expr='icontains')
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')  # Minimum price filter
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')  # Maximum price filter
    quantity = filters.NumberFilter(field_name='quantity', lookup_expr='gte')  # Filter by stock availability
    
    class Meta:
        model = Product
        fields = ['name', 'category', 'price_min', 'price_max', 'quantity']

class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ProductFilter
    ordering_fields = ['name', 'price', 'quantity', 'created_at']  # Define allowed ordering fields
    ordering = ['name']
    pagination_class = ProductPagination

    def get_permissions(self):
        if self.action in ['create', 'update']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
    

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

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        order = serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReviewViewset(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        order = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class WishlistViewset(ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        if created:
            return Response(WishlistSerializer(wishlist_item).data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Product already in wishlist'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        wishlist_item = self.get_object()
        wishlist_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class APIRootView(APIView):
    def get (self, request, *args, **kwargs):
        return Response({'products': request.build_absolute_uri('/api/products/'),
            #'users': request.build_absolute_uri('/api/users/'),
            'reviews': request.build_absolute_uri('/api/reviews/'),
            'categories': request.build_absolute_uri('/api/categories/'),
            'wishlist': request.build_absolute_uri('/api/wishlist/'),
            'products': request.build_absolute_uri('/api/products/'),
            'orders': request.build_absolute_uri('/api/orders/'),
            'discounts': request.build_absolute_uri('/api/discounts/'), 
        }, status = status.HTTP_200_OK)
    

class DiscountViewSet(ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return self.queryset
    
