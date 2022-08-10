from django.urls import path
from .views import *

urlpatterns = [
  path('place_order/', place_order, name='place_order'),
  path('payment/', payment, name='payment'),
  path('status/', payment_status, name='payment_status'),
  path('success/', payment_success, name='payment_success'),
  path('fail/', payment_fail, name='payment_fail')
]