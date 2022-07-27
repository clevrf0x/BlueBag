from django.contrib import admin
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
  list_display = ('name', 'slug', 'category', 'price', 'stock', 'is_available', 'created_date', 'modified_date')
  prepopulated_fields =  {'slug': ('name',)}
  
admin.site.register(Product, ProductAdmin)

