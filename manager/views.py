from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from django.contrib.auth.hashers import make_password, check_password

from accounts.models import Accounts
from manager.forms import ProductForm
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
    
    total_sales = 0
    orders = Order.objects.filter(is_ordered=True)
    for order in orders:
      total_sales += order.order_total
    
    context = {
      'user_count': user_count,
      'product_count': product_count,
      'order_count': order_count,
      'category_count': category_count,
      'total_sales': int(total_sales)
    }
    
    return render(request, 'manager/manager_dashboard.html', context)
  else:
    return redirect('home')
  

# change password

@never_cache
@login_required(login_url='manager_login')
def admin_change_password(request):
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
  
  return render(request, 'manager/admin_change_password.html')

# My orders
@login_required(login_url='manager_login')
def admin_order(request):
  current_user = request.user
  orders = Order.objects.filter(user=current_user, is_ordered=True).order_by('-created_at')
  context = {
    'orders': orders,
  }
  return render(request, 'manager/admin_orders.html', context)
  


# Product Management
@never_cache
@login_required(login_url='manager_login')
def manage_product(request):
  products = Product.objects.all().order_by('id')
  
  context = {
    'products': products
  }
  return render(request, 'manager/product_management.html', context)


# Delete Product
@never_cache
@login_required(login_url='manager_login')
def delete_product(request, product_id):
  product = Product.objects.get(id=product_id)
  product.delete()
  return redirect('manage_product')


# Add Product
@never_cache
@login_required(login_url='manager_login')
def add_product(request):
  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('manage_product')
  else:
    form = ProductForm()
    context = {
      'form': form
    }
    return render(request, 'manager/add_product.html', context)

# Edit Product
@never_cache
@login_required(login_url='manager_login')
def edit_product(request, product_id):
  product = Product.objects.get(id=product_id)
  form = ProductForm(instance=product)
  
  if request.method == 'POST':
    try:
      form = ProductForm(request.POST, request.FILES, instance=product)
      if form.is_valid():
        form.save()
        
        return redirect('manage_product')
    
    except Exception as e:
      raise e

  context = {
    'product': product,
    'form': form
  }
  return render(request, 'manager/edit_product.html', context)

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
