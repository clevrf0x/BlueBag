import datetime
from http.client import HTTPResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from cart.models import CartItem
from store.models import Product
from .models import Payment, OrderProduct, Order

from .forms import OrderForm, Order

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def payment_status(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }
    
    
    # authorize razorpay client with API Keys.
    razorpay_client = razorpay.Client(
      auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    client = razorpay_client
    try:
      status = client.utility.verify_payment_signature(params_dict)
      transaction = Payment.objects.get(order_id=response['razorpay_order_id'])
      transaction.status = status
      transaction.payment_id = response['razorpay_payment_id']
      transaction.save()
      
      # get order number
      order_number = transaction.order_number
      order = Order.objects.get(is_ordered=False, order_number=order_number)
      
      order.payment = transaction
      order.is_ordered = True
      order.save()
      
      cart_items = CartItem.objects.filter(user=order.user)
      for item in cart_items:
        order_product = OrderProduct()
        order_product.order_id = order.id
        order_product.payment = transaction
        order_product.user_id = order.user.id
        order_product.product_id = item.product_id
        order_product.quantity = item.quantity 
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()
        
        # Reducing Stock
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
        
        #  Clearing Cart Items
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        order_product = OrderProduct.objects.get(id=order_product.id)
        order_product.variation.set(product_variation)
        order_product.save()
      
      CartItem.objects.filter(user=order.user).delete()
      
      return redirect('payment_success')
    
    except Exception as e:
      raise e
      transaction = Payment.objects.get(order_id=response['razorpay_order_id'])
      transaction.delete()
      return redirect('payment_fail')
    



def payment_success(request):
  order_number = request.session['order_number']
  transaction_id = Payment.objects.get(order_number=order_number)
  
  try:
    order = Order.objects.get(order_number=order_number, is_ordered=True)
    ordered_products = OrderProduct.objects.filter(order_id=order.id)
    
    tax = 0
    total = 0
    grand_total = 0
    
    for item in ordered_products:
      total += (item.product_price * item.quantity)
      
    tax = total / 100
    grand_total = total + tax
    
    context = {
      'order': order,
      'ordered_products': ordered_products,
      'transaction_id': transaction_id,
      
      'total': total,
      'tax': tax,
      'grand_total': grand_total
    }
    
    return render(request, 'orders/success.html', context)
  
  except Exception as e:
    raise e

def payment_fail(request):
  return render(request, 'orders/fail.html')


@login_required(login_url='signin')
@csrf_exempt
def payment(request, total=0):
  current_user = request.user
  cart_item = CartItem.objects.filter(user=current_user)
  
  tax = 0
  grand_total = 0
  
  for item in cart_item:
    total += (item.product.price * item.quantity)
    
  tax = (1 * total) / 100
  grand_total = total + tax
  
  order_number = request.session['order_number']
  
  order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
  
  
  currency = 'INR'
  razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

  response_payment  = razorpay_client.order.create(dict(amount=int(grand_total) * 100,currency=currency))
  order_id = response_payment['id']
  order_status = response_payment['status']
  if order_status == 'created':
    payDetails = Payment(
      user = current_user,
      order_id = order_id,
      order_number = order_number,
      amount_paid = grand_total 
    )
    payDetails.save()

    
  context = {
    'order': order,
    'cart_items': cart_item,
    'total': total,
    'tax': tax,
    'grand_total': grand_total,
    
    'payment': response_payment,
    'razorpay_merchant_key':settings.RAZOR_KEY_ID,
    'grand_total': grand_total,
  }
  return render(request, 'orders/payments.html', context)


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
      
      request.session['order_number'] = order_number
      
      return redirect('payment')
    
    else:
      
      return redirect('checkout')
      