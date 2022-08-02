from itertools import product
from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, CartItem
from store.models import Product

from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def _get_cart_id(request):
  cart_id = request.session.session_key
  if not cart_id:
    cart_id = request.session.create()
  
  return cart_id


def add_cart(request, product_id):
  product = Product.objects.get(id=product_id)
  
  try:
    cart = Cart.objects.get(cart_id=_get_cart_id(request))
    
  except Cart.DoesNotExist:
    cart = Cart.objects.create(
      cart_id = _get_cart_id(request)
    )
    cart.save()
    
  try:
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.quantity += 1
    cart_item.save()
    
  except CartItem.DoesNotExist:
    cart_item = CartItem.objects.create(
      product = product,
      quantity = 1,
      cart = cart,
    )
    cart_item.save()
  return redirect('cart')


def remove_cart(request, product_id):
  cart = Cart.objects.get(cart_id=_get_cart_id(request))
  product = get_object_or_404(Product, id=product_id)
  cart_item = CartItem.objects.get(cart=cart, product=product)
  
  if cart_item.quantity > 1:
    cart_item.quantity -= 1
    cart_item.save()
  else:
    cart_item.delete()
    
  return redirect('cart')

def delete_cart(request, product_id):
  cart = Cart.objects.get(cart_id=_get_cart_id(request))
  product = get_object_or_404(Product, id=product_id)
  cart_item = CartItem.objects.get(cart=cart, product=product)

  cart_item.delete()
    
  return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
  try:
    cart = Cart.objects.get(cart_id=_get_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('product')
    
    for cart_item in cart_items:
      total += (cart_item.product.price * cart_item.quantity)
      # quantity += cart_item.quantity
    
    tax = (1 * total) / 100
    grand_total = total + tax
      
  except ObjectDoesNotExist:
    pass
  
  context = {
    'total': total,
    # 'quantity': quantity,
    'cart_items': cart_items,
    'tax': tax,
    'grand_total': grand_total,
  }
  return render(request, 'cart/cart.html', context)