from django.shortcuts import render, get_object_or_404
from .models import Product
from categories.models import Category

# Create your views here.

def store_home(request, category_slug=None):
  if category_slug is not None:
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, is_available=True)
    count = products.count()
  
  else:
    products = Product.objects.filter(is_available=True)
    count = products.count()
  
  context = {
    'products': products,
    'count': count,
    }
  return render(request, 'store/store.html', context)