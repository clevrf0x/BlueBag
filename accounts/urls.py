from django import views
from django.urls import path
from .views import *

urlpatterns = [
  path('', redirect_to_login),
  path('signin', signin, name='signin'),
  path('signup', signup, name='signup'),
  path('logout', logout_user, name='logout'),
  path('activate/<uidb64>/<token>/', activate, name='activate')
]