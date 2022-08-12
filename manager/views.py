from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from accounts.models import Accounts
from store.models import Product
from orders.models import Order
from categories.models import Category

# Create your views here.

@never_cache
@login_required(login_url='manager_login')
def manager_dashboard(request):
  if request.user.is_superadmin:
    
    user_count = Accounts.objects.filter(is_superadmin=False).count()
    product_count = Product.objects.all().count()
    order_count = Order.objects.filter(is_ordered=True).count()
    category_count = Category.objects.all().count()
    
    context = {
      'user_count': user_count,
      'product_count': product_count,
      'order_count': order_count,
      'category_count': category_count
    }
    
    return render(request, 'manager/manager_dashboard.html', context)
  else:
    return redirect('home')
  
  
# Manage Category
@never_cache
@login_required(login_url='manager_login')
def manage_category(request):
  
  return render(request, 'manager/category_management.html')


# User Management
@never_cache
@login_required(login_url='manager_login')
def manage_user(request):
  users = Accounts.objects.filter(is_superadmin=False) .order_by('id')
  context = {
    'users': users,
  }
  return render(request, 'manager/user_management.html', context)

# Ban User
@never_cache
@login_required(login_url='manager_login')
def ban_user(request, user_id):
  user = Accounts.objects.get(id=user_id)
  user.is_active = False
  user.save()

  return redirect('manage_user')

# UnBan User
@never_cache
@login_required(login_url='manager_login')
def unban_user(request, user_id):
  user = Accounts.objects.get(id=user_id)
  user.is_active = True
  user.save()

  return redirect('manage_user')


def redirect_to_login(request):
  return redirect('manager_login')

@never_cache
def manager_login(request):
  if request.user.is_authenticated:
    if request.user.is_superadmin:
      return redirect('manager_dashboard')
    else:
      return redirect('home')
  else:
    if request.method == 'POST':
      email = request.POST['email']
      password = request.POST['password']
      
      user = authenticate(request, username=email, password=password)
      if user is not None:
        if user.is_verified:
          if user.is_superadmin:
            login(request, user)
            return redirect('manager_dashboard')
          else:
            messages.warning(request, 'You are logged in a non-staff account')
        else:
          messages.warning(request, 'Your account is not verified. Please verify your account')

      else:
        messages.error(request, 'Email or Password is incorrect')
  return render(request, 'manager/manager_signin.html')

@never_cache
def manager_logout(request):
  logout(request)
  return redirect('manager_login')
