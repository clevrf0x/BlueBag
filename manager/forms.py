from django import forms
from store.models import Product
  
class ProductForm(forms.ModelForm):
  
  class Meta:
     model = Product
     fields = ['name', 'slug', 'description', 'price', 'images', 'category', 'stock', 'is_available', 'is_featured']
  
  def __init__(self, *args, **kwargs):
    super(ProductForm, self).__init__(*args, **kwargs)
    
    for field in self.fields:
      self.fields[field].widget.attrs['class'] = 'form-control'
    
    self.fields['is_available'].widget.attrs['class'] = 'ml-2 mt-1 form-check-input'
    self.fields['is_featured'].widget.attrs['class'] = 'ml-2 mt-1 form-check-input'
    