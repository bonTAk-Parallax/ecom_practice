import datetime
from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

  
class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=50, blank=True)

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=100, blank=False)
    photo = models.ImageField(upload_to='images/', verbose_name="Image")
    price = models.FloatField(blank=False)
    quantity = models.IntegerField( default=1)
    digital = models.BooleanField(default=False)

    def img_tag(self):
        if self.photo:
            return mark_safe('<img src="{}" width="60" height="50" />' .format(self.photo.url))
    img_tag.short_description = "Image"

    
    # def add_to_cart(self):
    #     self.quantity -= 1
    #     print(f"Added to cart: {self.name}")
    #     print(self.quantity)
    #     self.save()

    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    






    
