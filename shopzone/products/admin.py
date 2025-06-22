from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'stock', 'discount_percent']
    search_fields = ['name']
    list_filter = ['discount_percent', 'stock']
