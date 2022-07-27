from django.urls import path

from .views import *

urlpatterns = [
  path('', store_home, name='store_home'),
  path('<slug:category_slug>/', store_home, name='products_by_category'),
]