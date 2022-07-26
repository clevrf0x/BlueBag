from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.views.decorators.cache import never_cache

from .models import Accounts
from .forms import SignupForm

# User Verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
def redirect_to_login(request):
  return redirect('signin')


### Sign in Function
@never_cache
def signin(request):
  if request.user.is_authenticated:
    return redirect('home')
  else:
    if request.method == 'POST':
      email = request.POST['email']
      password = request.POST['password']
      
      user = authenticate(request, username=email, password=password)
      print(user)
      if user is not None:
        login(request, user)
        return redirect('home')
      
      else:
        messages.error(request, 'Email or Password is incorrect')
      
    return render(request, 'signin.html')


### Sign Up Function
@never_cache
def signup(request):
  if request.user.is_authenticated:
    return redirect('home')
  else:
    if request.method == 'POST':
      form = SignupForm(request.POST)
      if form.is_valid():
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        username = form.cleaned_data.get('username')
        phone_number = form.cleaned_data.get('phone_number')
        password = form.cleaned_data.get('password')
        
        user = Accounts.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        user.phone_number = phone_number
        user.save()
        
        # USER ACTIVATION
        current_site = get_current_site(request)
        mail_subject = "Please activate your account"
        message = render_to_string('email_verification.html', {
          'user': user,
          'domain': current_site,
          'uid': urlsafe_base64_encode(force_bytes(user.pk)),
          'token': default_token_generator.make_token(user),
        })
        to_mail = email
        send_email = EmailMessage(mail_subject, message, to=[to_mail])
        send_email.send()
        
        messages.success(request, "We send a verification email, Please confirm your email address")
        return redirect('signup')
        
    else:    
      form = SignupForm()
      
    context = {'form': form}
    return render(request, 'signup.html', context)

@never_cache
def logout_user(request):
  logout(request)
  return redirect('signin')

@never_cache
def activate(request, uidb64, token):
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = Accounts._default_manager.get(pk=uid)
  except(TypeError, ValueError, OverflowError, Accounts.DoesNotExist):
    user = None
    
  if user is not None and default_token_generator.check_token(user, token):
    user.is_active = True
    user.save()
    messages.success(request, "Congratulations! Your account is now activated")
    return redirect('signup')
  else:
    messages.error(request, "Invalid Activation link!!!")
    return redirect('signup')