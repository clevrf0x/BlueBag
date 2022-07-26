from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.

@never_cache
@login_required(login_url='manager_login')
def manager_dashboard(request):
  if request.user.is_superadmin:
    return render(request, 'manager_dashboard.html')
  else:
    return redirect('home')

def redirect_to_login(request):
  return redirect('manager_login')

@never_cache
def manager_login(request):
  if request.user.is_authenticated:
    if request.user.is_superadmin:
      return redirect('manager_dashboard')
    else:
      return redirect('home')
  else:
    if request.method == 'POST':
      email = request.POST['email']
      password = request.POST['password']
      
      user = authenticate(request, username=email, password=password)
      if user is not None:
        if user.is_verified:
          if user.is_superadmin:
            login(request, user)
            return redirect('manager_dashboard')
          else:
            messages.warning(request, 'You are logged in a non-staff account')
        else:
          messages.warning(request, 'Your account is not verified. Please verify your account')

      else:
        messages.error(request, 'Email or Password is incorrect')
  return render(request, 'manager_signin.html')

@never_cache
def manager_logout(request):
  logout(request)
  return redirect('manager_login')
