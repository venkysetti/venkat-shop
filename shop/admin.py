from django.contrib import admin
from .category import Category
from .product import Product
from .costomer import Customer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'cat', 'created_at']
    list_filter = ['cat']
    search_fields = ['name', 'desc']
class Customerinfo(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile']
    search_fields = ['name', 'email', 'mobile']

admin.site.register(Customer,Customerinfo)
