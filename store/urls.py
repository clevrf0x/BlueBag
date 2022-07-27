from django.urls import path

from .views import *

urlpatterns = [
  path('', store_home, name='store_home'),
  path('<slug:category_slug>/', store_home, name='products_by_category'),
  path('<slug:category_slug>/<slug:product_slug>/', product_details, name='product_details'),
]