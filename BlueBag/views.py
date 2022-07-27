
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from store.models import Product

@never_cache
def home(request):
  products = Product.objects.all().filter(is_available=True, is_featured=True)
  
  context = { 'products': products }
  return render(request, 'index.html', context)