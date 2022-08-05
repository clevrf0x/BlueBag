import datetime
from locale import currency
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from cart.models import CartItem

from .forms import OrderForm, Order

# Create your views here.
@login_required(login_url='signin')
def place_order(request, total=0, quantity=0):
  current_user = request.user
  
  cart_item = CartItem.objects.filter(user=current_user)
  if cart_item.count() < 1:
    return redirect('store_home')
  
  tax = 0
  grand_total = 0
  
  for item in cart_item:
    total += (item.product.price * item.quantity)
    quantity += item.quantity
    
  tax = (1 * total) / 100
  grand_total = total + tax
  
  
  if request.method == 'POST':
    form = OrderForm(request.POST)
    
    if form.is_valid():
      # Store billing address and details to Order table
      data = Order()
      
      data.user = current_user
      data.firstname = form.cleaned_data['firstname']
      data.lastname = form.cleaned_data['lastname']
      data.email = form.cleaned_data['email']
      data.phone_number = form.cleaned_data['phone_number']
      data.address_line_1 = form.cleaned_data['address_line_1']
      data.address_line_2 = form.cleaned_data['address_line_2']
      data.city = form.cleaned_data['city']
      data.state = form.cleaned_data['state']
      data.zipcode = form.cleaned_data['zipcode']
      data.order_note = form.cleaned_data['order_note']
      data.order_total = grand_total
      data.tax = tax
      data.ip = request.META.get('REMOTE_ADDR')
      data.save()

      # Generate Order number
      year = int(datetime.date.today().strftime('%Y'))
      month = int(datetime.date.today().strftime('%m'))
      date = int(datetime.date.today().strftime('%d'))
      d = datetime.date(year, month, date)
      current_date = d.strftime("%Y%m%d")
      order_number = current_date + str(data.id)
      data.order_number = order_number
      data.save()
      
      return redirect('checkout')
    
    else:
      return redirect('checkout')
      