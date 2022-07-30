from .models import Cart, CartItem
from .views import _get_cart_id

def cart_counter(request):
  cart_count = 0
  if 'admin' in request.path:
    return {}
  
  else:
    try:
      cart = Cart.objects.get(cart_id=_get_cart_id(request))
      cart_items = CartItem.objects.filter(cart=cart)
      for cart_item in cart_items:
        cart_count = cart_items.count()
        
    except Cart.DoesNotExist:
      cart_count = 0
      
  return dict(cart_count=cart_count)