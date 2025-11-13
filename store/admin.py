
from django.contrib import admin
from .models import Product, DiscountRule


class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'base_price', 'stock_quantity', 'current_price', 'is_active') 
   
    list_editable = ('base_price', 'stock_quantity', 'is_active') 
    
    readonly_fields = ('current_price',) 

admin.site.register(Product, ProductAdmin)
admin.site.register(DiscountRule)