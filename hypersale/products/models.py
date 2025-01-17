from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)  
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Currency code (ISO 4217 format)."
    )
    currency = models.CharField(
        max_length=3,
        choices=[
            ('USD', 'US Dollar'),
            ('EUR', 'Euro'),
            ('GBP', 'British Pound')
        ],
        default='USD',
        help_text="Currency code (ISO 4217 format)."
    )
    image_url = models.ImageField(
        upload_to='image_url/', default='default.jpg', 
        blank = True, null=True
    )
   
    quantity = models.PositiveIntegerField(
        default=0, help_text="Stock quantity available"
    )
    created_at = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, related_name='products')

    def __str__(self):
        return f"{self.name} - {self.price} {self.currency}"
    
    def reduce_stock(self, quantity: int):
        if quantity > self.quantity:
            raise ValueError("Not enough stock available")
        self.quantity -= quantity
        self.save()

    def get_discounted_price(self):
        active_discounts = self.discounts.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now())
        price = self.price
        for discount in active_discounts:
            price = discount.apply_discount(price)
        return price
    
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, through='OrderProduct')
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(
        max_digits=10, decimal_places=2, 
        help_text="Total cost of the order.", 
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length= 10,
        choices=[
            ('Pending', 'Pending'),
            ('Shipped', 'Shipped'),
            ('Completed', 'Completed'),
        ], default = 'Pending',
    )

    def __str__(self):
        return f"Order {self.id} - {self.total}"
    
    def calculate_total(self):
        total = 0

        try:
        # Use the default related manager `orderproduct_set` if no `related_name` was provided
            order_products = self.order_products.all()  # Adjust this if a `related_name` exists on the FK
        except AttributeError:
            raise AttributeError(
            f"The 'Order' model does not have a default reverse relation 'orderproduct_set")
            

        for order_product in order_products:
            total += order_product.quantity * order_product.product.price

        self.total = total
        self.save()


    

    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='order_products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order {self.order.id}"   

    def reduce_stock(self, quantity):
        self.product.quantity -= quantity
        self.product.save()
        
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    user=models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now = True)

    class Meta:
        unique_together = ['user', 'product']

class Discount(models.Model):
    product = models.ForeignKey('Product', related_name='discounts', on_delete=models.CASCADE)
    discount_type = models.CharField(max_length=10, choices=[('percentage', 'Percentage'), ('amount', 'Amount')])
    value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def apply_discount(self, price):
        if self.discount_type == 'percentage':
            return price * (1 - (self.value / 100))
        elif self.discount_type == 'amount':
            return price - self.value
        return price

    def __str__(self):
        return f"Discount on {self.product.name}"