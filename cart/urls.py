from django.urls import path
from .views import *

urlpatterns = [
  path('', cart, name="cart")
]