from django.db import models
from django.urls import reverse
from categories.models import Category

# Create your models here.
class Product(models.Model):
  name = models.CharField(max_length=255, unique=True)
  slug = models.SlugField(max_length=255, unique=True)
  description = models.TextField(max_length=2500, blank=True)
  price = models.IntegerField()
  images = models.ImageField(upload_to="photos/products")
  stock = models.IntegerField()
  is_available = models.BooleanField(default=True)
  is_featured = models.BooleanField(default=False)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)
  
  def get_url(self):
    return reverse('product_details', args=[self.category.slug, self.slug])
  
  def __str__(self):
    return self.name
  
class VariationManager(models.Manager):
  def colors(self):
    return super(VariationManager, self).filter(variation_category='color', is_active=True)
  
  def sizes(self):
    return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_choices = (
  ('color', 'Color'),
  ('size', 'Size'),
)

class Variation(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  variation_category = models.CharField(max_length=100, choices=variation_choices)
  variation_value = models.CharField(max_length=100)
  is_active = models.BooleanField(default=True)
  created_date = models.DateTimeField(auto_now_add=True)
  
  objects = VariationManager()
  
  def __str__(self):
    return self.variation_value
