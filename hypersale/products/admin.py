from django.contrib import admin
from .models import Product, Order, Category, OrderProduct

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'price','currency']
    search_fields= ['name', 'quantity', 'price']

admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields= ['name', 'description']

admin.site.register(Category, CategoryAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'total','created_at', 'status']
    search_fields= ['id', 'status', 'created_at']

admin.site.register(Order, OrderAdmin)
# Register your models here.
