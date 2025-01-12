from ssl import create_default_context
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)  
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
    quantity = models.PositiveIntegerField(
        default=0, help_text="Stock quantity available"
    )
    created_at = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, related_name='products')

    def __str__(self):
        return f"{self.name} - {self.price} {self.currency}"
    

    
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    products = models.ManyToManyField(Product, through="OrderProduct")
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

    def calculate_total (self):
        total_cost = sum(
            item.product.price * item.quantity for item in self.orderproduct_set.all()
        )
        self.total = total_cost
        self.save()
        return total_cost
    
    def __str__(self):
        return f"Order #{self.id} - Total: {self.total}"
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order {self.order.id}"    
        






# Create your models here.
