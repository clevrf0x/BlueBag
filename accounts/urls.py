from django import views
from django.urls import path
from .views import *

urlpatterns = [
  path('', redirect_to_login),
  path('signin', signin, name='signin'),
  path('signup', signup, name='signup'),
  path('logout', logout_user, name='logout'),
  path('activate/<uidb64>/<token>/', activate, name='activate'),
  
  path('user_dashboard/', user_dashboard, name='user_dashboard'),
  path('my_orders/', my_order, name='my_orders'),
  path('cancel_order/<int:order_number>/', cancel_order, name='cancel_order'),
  path('view_order/<int:order_number>/', view_order, name='view_order'),
]