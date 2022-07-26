from django import forms
from .models import Accounts

class SignupForm(forms.ModelForm):
  
  # Password fields
  password = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Enter Password'
  }))
  
  confirm_password =  forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Repeat Password',
  }))
  
  class Meta:
    model = Accounts
    fields = ['first_name', 'last_name', 'email', 'username', 'phone_number', 'password']
    
    
  def clean(self):
    cleaned_data = super(SignupForm, self).clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')
    
    if password != confirm_password:
      raise forms.ValidationError("Password doesn't match")
    
    
  def __init__(self, *args, **kwargs):
    super(SignupForm, self).__init__(*args, **kwargs)
    
    self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First name'
    self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last name'
    self.fields['email'].widget.attrs['placeholder'] = 'Enter Email address'
    self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone number'
    self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
    
    
    for field in self.fields:
      self.fields[field].widget.attrs['class'] = 'form-control'
  