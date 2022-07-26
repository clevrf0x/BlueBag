from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

# Custom User Model Manager
class MyAccountManager(BaseUserManager):
  def create_user(self, first_name, last_name, username, email, password=None):
    if not email:
      raise ValueError('Email address is required')
    
    if not username:
      raise ValueError('Username is required')
    
    user = self.model(
      email = self.normalize_email(email),
      username = username,
      first_name = first_name,
      last_name = last_name,
    )
    
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self, first_name, last_name, username, email, password):
    user = self.create_user(
      email = self.normalize_email(email),
      username = username,
      password = password,
      first_name = first_name,
      last_name = last_name,
    )
    
    user.is_admin = True
    user.is_superadmin = True
    user.is_active = True
    user.is_staff = True
    user.is_verified = True
    
    user.save(using=self._db)
    return user
  
  
# Custom User Model
class Accounts(AbstractBaseUser):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  email = models.EmailField(max_length=100, unique=True)
  username = models.CharField(max_length=100, unique=True)
  phone_number = models.CharField(max_length=10)
  
  #required 
  date_joined = models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(auto_now_add=True)
  is_admin = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_verified = models.BooleanField(default=False)
  is_superadmin = models.BooleanField(default=False)
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
  
  objects = MyAccountManager()
  
  class Meta:
    verbose_name_plural = 'Accounts'
  
  
  def __str__(self):
    return self.email
  
  def has_perm(self, perm, obj=None):
    return self.is_admin
  
  def has_module_perms(self, add_label):
    return True