from django.shortcuts import render, get_object_or_404
from .models import Product
from categories.models import Category

from django.db.models import Q

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from cart.views import _get_cart_id
from cart.models import CartItem

# Create your views here.

def store_home(request, category_slug=None):
  if category_slug is not None:
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, is_available=True).order_by('-created_date')
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    count = products.count()
  
  else:
    products = Product.objects.filter(is_available=True).order_by('-created_date')
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    count = products.count()
  
  context = {
    'products': paged_products,
    'count': count,
    }
  return render(request, 'store/store.html', context)


def product_details(request, category_slug, product_slug):
  try:
    product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id=_get_cart_id(request), product=product).exists()
  except Exception as e:
    raise e
  
  context = {
    'product': product,
    'in_cart': in_cart
  }
  return render(request, 'store/product_details.html', context)


def search(request):
  products = None
  count = 0
  
  if 'keyword' in request.GET:
    keyword = request.GET['keyword']
    if keyword:
      products = Product.objects.filter(Q(description__icontains=keyword) or Q(name__icontains=keyword)).order_by('-created_date')
      count = products.count()
    
    
  context = {
    'products': products,
    'count': count,
    }
  return render(request, 'store/store.html', context)