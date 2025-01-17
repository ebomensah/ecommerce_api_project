from rest_framework import serializers
from .models import Wishlist, Category, Product, Order, OrderProduct, Review, Discount 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)  

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'currency', 'quantity', 'created_at', 'category', 'image_url']
        read_only_fields = ['created_at']

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']

    def validate(self, attrs):
        # You can validate product stock here if needed
        product = attrs['product']
        quantity = attrs['quantity']

        if product.quantity < quantity:
            raise serializers.ValidationError(f"Not enough stock for {product.name}. Only {product.quantity} available.")
        
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True, required=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Set current user for the order

    class Meta:
        model = Order
        fields = ['id', 'status', 'user', 'total', 'order_products']
        read_only_fields = ['total']  # total should not be written directly by the user

    
    def create(self, validated_data):
        order_products_data = validated_data.pop('order_products', [])
        order = Order.objects.create(**validated_data)

        for order_product_data in order_products_data:
            product = order_product_data['product']
            quantity = order_product_data['quantity']

            # Make sure there's enough stock
            if quantity > product.quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for {product.name}. Only {product.quantity} available."
                )

            # Create the OrderProduct objects (intermediary)
            order_product = OrderProduct.objects.create(order=order, product=product, quantity=quantity)

            # Decrease stock
            product.reduce_stock(quantity)

        # Recalculate the total price for the order
        order.calculate_total()
        return order

    def update(self, instance, validated_data):
        order_products_data = validated_data.pop('order_products', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Delete old order products and create new ones
        instance.orderproduct_set.all().delete()  # Using reverse relation manager
        for order_product_data in order_products_data:
            product = order_product_data['product']
            quantity = order_product_data['quantity']

            order_product = OrderProduct.objects.create(order=instance, product=product, quantity=quantity)
            product.reduce_stock(quantity)

        # Recalculate the order total
        instance.calculate_total()
        return instance


    

    def validate(self, attrs):
        order_products = attrs.get('order_products', [])

        # Pass the products into context for nested validation in OrderProductSerializer
        for order_product in order_products:
            order_product['product'] = Product.objects.get(id=order_product['product'].id)

        return attrs

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['product', 'user', 'created_at']
        read_only_fields = ['user']


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'product', 'discount_type', 'value', 'start_date', 'end_date', 'created_by']
        read_only_fields = ['created_by']


    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)