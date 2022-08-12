from django.urls import path
from .views import *

urlpatterns = [
  path('', redirect_to_login),
  path('login', manager_login, name='manager_login'),
  path('logout', manager_logout, name='manager_logout'),
  path('dashboard', manager_dashboard, name='manager_dashboard'),
  path('manage_user', manage_user, name='manage_user'),
  path('manage_category/', manage_category, name='manage_category'),
  path('add_category/', add_category, name='add_category'),
  
  path('update_category/<int:category_id>/', update_category, name="update_category"),
  path('delete_category/<int:category_id>/', delete_category, name="delete_category"),
  
  path('ban_user/<int:user_id>/', ban_user, name='ban_user'),
  path('unban_user/<int:user_id>/', unban_user, name='unban_user'),
  
]