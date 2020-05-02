from django.db import models
from django.urls import reverse
from django.conf import settings
from datetime import datetime
# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE , default=1)
    name = models.CharField(max_length=100)
    amt = models.IntegerField(default=0)
    recursive= models.BooleanField(max_length=100,default=False) 
    pay_type = models.CharField(max_length=50)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)   
    
    def __str__(self):
        return self.name

class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE ,related_name='category', default=1)
    name = models.CharField(max_length=100)
    amt = models.IntegerField(default=0)
    budget = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Sub_Category(models.Model):
    name = models.CharField(max_length=100)
    amt = models.IntegerField(default=0)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='sub_category',null=True,blank=True)

    def __str__(self):
        return self.name

class Year(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE ,related_name='user_year', default=1)
    name = models.IntegerField()
    annual_income = models.IntegerField(default=0)
    annual_expenditure =  models.IntegerField(default=0)
    def __int__(self):
        return self.name

class Month(models.Model):
    name = models.CharField(max_length=50)
    monthly_income = models.IntegerField(default=0)
    monthly_expenditure =  models.IntegerField(default=0)
    year_link = models.ForeignKey(Year ,on_delete=models.CASCADE,related_name='yr',null=True,blank=True)
    def __str__(self):
        return self.name

class Data(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE ,related_name='dataset', default=1)
    sub_category = models.ForeignKey(Sub_Category,on_delete=models.CASCADE,related_name='datas',null=True,blank=True)
    spent = models.IntegerField()
    balance = models.IntegerField(blank=True,null=True)
    recursive= models.BooleanField(max_length=100) 
    pay_type = models.CharField(max_length=50)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(default=datetime.now, blank=True)   
    month_link = models.ForeignKey(Month ,on_delete=models.CASCADE,related_name='mon',null=True,blank=True)
    def __str__(self):
        return str(self.spent)
    
    def get_absolute_url(self):
        return reverse("expense:post_detail",kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp","-updated"]

