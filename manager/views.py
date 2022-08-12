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
  
  

# Manage Order
@never_cache
@login_required(login_url='manager_login')
def manage_order(request):
  orders = Order.objects.filter(is_ordered=True).order_by('-order_number')
  
  context = {
    'orders': orders
  }
  return render(request, 'manager/order_management.html', context)


# Cancel Order
@never_cache
@login_required(login_url='manager_login')
def cancel_order(request, order_number):
  order = Order.objects.get(order_number=order_number)
  order.status = 'Cancelled'
  order.save()
  
  return redirect('manage_order')
  

# Accept Order
@never_cache
@login_required(login_url='manager_login')
def accept_order(request, order_number):
  order = Order.objects.get(order_number=order_number)
  order.status = 'Accepted'
  order.save()
  
  return redirect('manage_order')

# Complete Order
@never_cache
@login_required(login_url='manager_login')
def complete_order(request, order_number):
  order = Order.objects.get(order_number=order_number)
  order.status = 'Completed'
  order.save()
  
  return redirect('manage_order')
  
  
# Manage Category
@never_cache
@login_required(login_url='manager_login')
def manage_category(request):
  categories = Category.objects.all().order_by('id')
  
  context = {
    'categories': categories
  }
  
  return render(request, 'manager/category_management.html', context)


# Add category
@never_cache
@login_required(login_url='manager_login')
def add_category(request):
  if request.method == 'POST':
    try:
      category_name = request.POST['category_name']
      category_slug = request.POST['category_slug']
      category_description = request.POST['category_description']
      
      category = Category(
        name = category_name,
        slug = category_slug,
        description = category_description
      )
      
      category.save()
      return redirect('manage_category')
    
    except Exception as e:
      raise e
  
  return render(request, 'manager/category_add.html')


# Update Category
@never_cache
@login_required(login_url='manager_login')
def update_category(request, category_id):
  try:
    category = Category.objects.get(id=category_id)
    
    if request.method == 'POST':
      category_name = request.POST['category_name']
      category_slug = request.POST['category_slug']
      category_description = request.POST['category_description']
      
      category.name = category_name
      category.slug = category_slug
      category.description = category_description
      category.save()
      
      return redirect('manage_category')
    
    context = {
      'category': category
    }
    return render(request, 'manager/category_update.html', context)
    
  except Exception as e:
    raise e


# Delete Category
@never_cache
@login_required(login_url='manager_login')
def delete_category(request, category_id):
  category = Category.objects.get(id=category_id)
  category.delete()
  
  return redirect('manage_category')

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
