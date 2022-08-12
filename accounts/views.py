from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.hashers import check_password, make_password
import requests

from orders.models import Order, OrderProduct, Payment

from .models import Accounts
from .forms import SignupForm

from cart.models import Cart, CartItem
from cart.views import _get_cart_id

# User Verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
def redirect_to_login(request):
  return redirect('signin')

@login_required(login_url='signin')
def user_dashboard(request):
  
  try:
    current_user = request.user
    total_orders = Order.objects.filter(user=current_user, is_ordered=True).count()
    
    context = {
      'current_user': current_user,
      'total_orders': total_orders
    }
    
    return render(request, 'user_dashboard.html', context)
  
  except Exception as e:
    raise e
  
@login_required(login_url='signin')
def my_order(request):
  current_user = request.user
  orders = Order.objects.filter(user=current_user, is_ordered=True).order_by('-created_at')
  context = {
    'orders': orders,
  }
  return render(request, 'my_orders.html', context)

@login_required(login_url='signin')
def cancel_order(request, order_number):
  try:
    order = Order.objects.get(order_number=order_number)
    order.status = "Cancelled"
    order.save()
    
    return redirect('my_orders')
    
  except Exception as e:
    raise e
  
@login_required(login_url='signin')
def view_order(request, order_number):
  try:
    order = Order.objects.get(order_number=order_number)
    ordered_products = OrderProduct.objects.filter(order_id=order.id)
    transaction_id = Payment.objects.get(order_number=order_number)
    
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
    
    return render(request, 'orders/view_order.html', context)
    
  except Exception as e:
    raise e

@never_cache
@login_required(login_url='signin')
def change_password(request):
  if request.method == 'POST':
    current_user = request.user
    current_password = request.POST['current_password']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    
    if password == confirm_password:
      if check_password(current_password, current_user.password):
        if check_password(password, current_user.password):
          messages.warning(request, 'Current password and new password is same')
        else:
          hashed_password = make_password(password)
          current_user.password = hashed_password
          current_user.save()
          messages.success(request, 'Password changed successfully')
      else:
        messages.error(request, 'Wrong password')
    else:
      messages.error(request, 'Passwords does not match')
  
  return render(request, 'accounts/change_password.html')

### Sign in Function
@never_cache
def signin(request):
  if request.user.is_authenticated:
    return redirect('home')
  else:
    if request.method == 'POST':
      email = request.POST['email']
      password = request.POST['password']
      
      user = authenticate(request, username=email, password=password)
      if user is not None:
        if user.is_verified:
          
          try:
            cart = Cart.objects.get(cart_id=_get_cart_id(request)) 
            is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
            if is_cart_item_exists:
              cart_item = CartItem.objects.filter(cart=cart)
              
              # Get product variation by cart id
              product_variation = []
              for item in cart_item:
                variation = item.variations.all()
                product_variation.append(list(variation))
              
              # Get cart item from user to access product variation
              cart_item = CartItem.objects.filter(user=user)
              existing_variations_list = []
              id = []
              for item in cart_item:
                existing_variations = item.variations.all()
                existing_variations_list.append(list(existing_variations))
                id.append(item.id)
              
              for variation in product_variation:
                if variation in existing_variations_list:
                  index = existing_variations_list.index(variation)
                  item_id = id[index]
                  item = CartItem.objects.get(id=item_id)
                  item.quantity += 1
                  item.user = user
                  item.save()

                else:
                  cart_item = CartItem.objects.filter(cart=cart)
                  for item in cart_item:
                    item.user = user
                    item.save()
          except:
            pass
          
          login(request, user)
          url = request.META.get('HTTP_REFERER')
          
          try:
            query = requests.utils.urlparse(url).query
            params = dict(x.split('=') for x in query.split('&'))
            if 'next' in params:
              next_page = params['next']
              return redirect(next_page)
            
          except:
            return redirect('home')
    
        else:
          messages.warning(request, 'Account is not activated, Please activate your account to login')
      
      else:
        messages.error(request, 'Email or Password is incorrect')
      
    return render(request, 'signin.html')


### Sign Up Function
@never_cache
def signup(request):
  if request.user.is_authenticated:
    return redirect('home')
  else:
    if request.method == 'POST':
      form = SignupForm(request.POST)
      if form.is_valid():
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        username = form.cleaned_data.get('username')
        phone_number = form.cleaned_data.get('phone_number')
        password = form.cleaned_data.get('password')
        
        user = Accounts.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        user.phone_number = phone_number
        user.save()
        
        # USER ACTIVATION
        current_site = get_current_site(request)
        mail_subject = "Please activate your account"
        message = render_to_string('email_verification.html', {
          'user': user,
          'domain': current_site,
          'uid': urlsafe_base64_encode(force_bytes(user.pk)),
          'token': default_token_generator.make_token(user),
        })
        to_mail = email
        send_email = EmailMessage(mail_subject, message, to=[to_mail])
        send_email.send()
        
        messages.success(request, "We send a verification email, Please confirm your email address")
        return redirect('signin')
        
    else:    
      form = SignupForm()
      
    context = {'form': form}
    return render(request, 'signup.html', context)

@never_cache
def logout_user(request):
  logout(request)
  return redirect('signin')

@never_cache
def activate(request, uidb64, token):
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = Accounts._default_manager.get(pk=uid)
  except(TypeError, ValueError, OverflowError, Accounts.DoesNotExist):
    user = None
    
  if user is not None and default_token_generator.check_token(user, token):
    user.is_verified = True
    user.save()
    messages.success(request, "Congratulations! Your account is now activated")
    return redirect('signin')
  else:
    messages.error(request, "Invalid Activation link!!!")
    return redirect('signin')