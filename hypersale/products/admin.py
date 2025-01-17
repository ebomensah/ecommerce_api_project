from django.contrib import admin
from .models import Product, Order, Category, Discount, Wishlist, Review, OrderProduct

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'price','currency', 'image_url']
    search_fields= ['name', 'quantity', 'price']

admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields= ['name', 'description']

admin.site.register(Category, CategoryAdmin)

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1  
    fields = ['product', 'quantity']
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'total','created_at', 'status']
    search_fields= ['id', 'status', 'created_at']
    inlines = [OrderProductInline]

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser: 
            return ['status']  
        return super().get_readonly_fields(request, obj)

    def save_model(self, request, obj, form, change):
        if not change: 
            obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Order, OrderAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    fields = ('product', 'rating', 'comment')  # Exclude user from the fields

    def save_model(self, request, obj, form, change):
        if not change:  # Only set user on creation, not on update
            obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Review, ReviewAdmin)

class WishlistAdmin (admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    fields = ['product']

    def save_model(self, request, obj, form, change):
        if not change:  # Only set user on creation, not on update
            obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Wishlist, WishlistAdmin)

class DiscountAdmin(admin.ModelAdmin):
    list_display = ['product', 'discount_type', 'value', 'start_date', 'end_date']
    exclude = ['created_by']
    
 

admin.site.register(Discount, DiscountAdmin)
# Register your models here.
