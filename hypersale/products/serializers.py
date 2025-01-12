from rest_framework import serializers
from .models import Category, Product, Order, OrderProduct


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)  # Nested serialization for categories

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'currency', 'quantity', 'created_at', 'category']
        read_only_fields = ['created_at']


class OrderProductSerializer(serializers.ModelSerializer):
   #product = ProductSerializer()  # Nested serialization for product details

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True, required=False)
   
    class Meta:
        model = Order
        fields = ['id', 'status', 'products', 'total', 'order_products']
        read_only_fields = ['total']


    def create(self, validated_data):
        order_products_data = validated_data.pop('order_products', [])
        
        order = Order.objects.create(**validated_data)

        for order_product_data in order_products_data:
            product = order_product_data['product']
            quantity = order_product_data['quantity']
            OrderProduct.objects.create(order=order, product=product, quantity=quantity)
        
        order.calculate_total()
        return order

    def update(self, instance, validated_data):
        # Similar to 'create', but for updates
        order_products_data = validated_data.pop('order_products', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Delete old order_product associations and create new ones
        instance.orderproduct_set.all().delete()
        for order_product_data in order_products_data:
            OrderProduct.objects.create(order=instance, 
                                        product=order_product_data['product'], 
                                        quantity=order_product_data['quantity'])

        # Recalculate the total for the updated order
        instance.calculate_total()
        return instance