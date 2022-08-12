from django.urls import path
from .views import *

urlpatterns = [
  path('', redirect_to_login),
  path('login', manager_login, name='manager_login'),
  path('logout', manager_logout, name='manager_logout'),
  path('dashboard', manager_dashboard, name='manager_dashboard'),
  path('manage_user', manage_user, name='manage_user'),
  path('manage_category/', manage_category, name='manage_category'),
  
  path('ban_user/<int:user_id>/', ban_user, name='ban_user'),
  path('unban_user/<int:user_id>/', unban_user, name='unban_user'),
  
]