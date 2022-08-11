from django.contrib import admin
from .models import Order, OrderProduct, Payment

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
  list_display = ['user', 'payment', 'order_number', 'order_total', 'status', 'is_ordered', 'created_at']
  list_editable = ('status',)
  list_filter = ('user', 'status', 'is_ordered', 'created_at')
  
class OrderProductAdmin(admin.ModelAdmin):
  list_display = ['order', 'payment', 'user', 'product', 'quantity', 'product_price', 'ordered', 'created_at']
  list_filter = ('user', 'ordered', 'created_at')

class PaymentAdmin(admin.ModelAdmin):
  list_display = ['user', 'payment_id', 'order_number', 'order_id', 'amount_paid', 'status', 'payment_method', 'created_at']
  list_editable = ('status',)
  list_filter = ('user', 'status', 'created_at')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Payment, PaymentAdmin)