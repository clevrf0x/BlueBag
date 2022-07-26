from django.urls import path
from .views import *

urlpatterns = [
  path('', redirect_to_login),
  path('login', manager_login, name='manager_login'),
  path('logout', manager_logout, name='manager_logout'),
  path('dashboard', manager_dashboard, name='manager_dashboard')
]