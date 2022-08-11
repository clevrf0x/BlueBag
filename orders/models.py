from django.db import models

from accounts.models import Accounts
from store.models import Product, Variation
# Create your models here.

class Payment(models.Model):
  user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
  payment_id = models.CharField(max_length=100)
  order_id = models.CharField(max_length=130,blank=True)
  order_number = models.CharField(max_length=50, blank=True)
  payment_method = models.CharField(max_length=100, default='RazorPay')
  amount_paid = models.CharField(max_length=100)
  status = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.payment_id


class Order(models.Model):
  STATUS = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
  )
  
  user = models.ForeignKey(Accounts, on_delete=models.SET_NULL, null=True)
  payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
  order_number = models.CharField(max_length=50)
  firstname = models.CharField(max_length=50)
  lastname = models.CharField(max_length=50)
  phone_number = models.CharField(max_length=15)
  email = models.EmailField(max_length=50)
  address_line_1 = models.CharField(max_length=200)
  address_line_2 = models.CharField(max_length=200)
  zipcode = models.CharField(max_length=10)
  state = models.CharField(max_length=50)
  city = models.CharField(max_length=50)
  order_note = models.CharField(max_length=250, blank=True) 
  order_total = models.FloatField()
  tax = models.FloatField()
  status = models.CharField(max_length=15, choices=STATUS, default='Pending')
  ip = models.CharField(max_length=20, blank=True)
  is_ordered = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def full_name(self):
    return f'{self.firstname} {self.lastname}'
  
  def full_address(self):
    return f'{self.address_line_1} {self.address_line_2}'
  
  def __str__(self):
    return self.order_number
  

class OrderProduct(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
  user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  variation = models.ManyToManyField(Variation, blank=True)
  quantity = models.IntegerField()
  product_price = models.FloatField()
  ordered = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.order.order_number