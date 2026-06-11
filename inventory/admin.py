from django.contrib import admin
from .models import Category, Product, Sale


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'quantity', 'barcode_code']
    list_filter = ['category']
    search_fields = ['name', 'barcode_code']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'unit_price', 'total_price', 'sold_at']
    list_filter = ['sold_at']
    search_fields = ['product__name', 'product__barcode_code']
    readonly_fields = ['unit_price', 'total_price', 'sold_at']
