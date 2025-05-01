from django.contrib import admin
from .models import Product, Customer, Sale

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer', 'quantity', 'date', 'get_total')
    list_filter = ('date', 'product', 'customer')
    date_hierarchy = 'date'
    
    def get_total(self, obj):
        return f"${obj.total_amount}"
    get_total.short_description = 'Total'
