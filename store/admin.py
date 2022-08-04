from django.contrib import admin
from .models import Product, Variation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
  list_display = ('name', 'slug', 'category', 'price', 'stock', 'is_available', 'is_featured', 'created_date', 'modified_date')
  prepopulated_fields =  {'slug': ('name',)}
  
class VariationAdmin(admin.ModelAdmin):
  list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_date')
  list_editable = ('is_active',)
  list_filter = ('product', 'variation_category', 'variation_value')
  
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)