from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
  class Meta:
    model = Order
    fields = ['firstname', 'lastname', 'email', 'phone_number', 'address_line_1', 'address_line_2', 'city', 'state', 'zipcode', 'order_note']