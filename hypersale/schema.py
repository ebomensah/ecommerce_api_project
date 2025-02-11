# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountsCustomuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    username = models.CharField(unique=True, max_length=220)
    email = models.CharField(unique=True, max_length=254)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'accounts_customuser'


class AccountsCustomuserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING)
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'accounts_customuser_groups'
        unique_together = (('customuser', 'group_id'),)


class AccountsCustomuserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser_id = models.BigIntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'accounts_customuser_user_permissions'


class ProductsCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'products_category'


class ProductsOrder(models.Model):
    created_at = models.DateTimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'products_order'


class ProductsOrderproduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(ProductsOrder, models.DO_NOTHING)
    product = models.ForeignKey('ProductsProduct', models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'products_orderproduct'


class ProductsProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'products_product'


class ProductsProductCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(ProductsProduct, models.DO_NOTHING)
    category = models.ForeignKey(ProductsCategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'products_product_category'
        unique_together = (('product', 'category'),)
