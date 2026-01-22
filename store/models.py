from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import AbstractUser
from django.conf import settings


  
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


    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True )
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    @property
    def total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.price for item in orderitems])
        return total
    
    def rollback(self):
        print("this is rollback function within ORDER")
        for item in self.orderitem_set.all():
            item.cart_rollback()



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    item_quantity = models.PositiveIntegerField(default=0, null=True, blank=True)

    def add_to_cart(self):
        self.item_quantity += 1
        self.item.quantity -= 1
        self.item.save()
        self.save()

    def cart_rollback(self):
        print("rollback funftion within ORDERITEM")
        self.item.quantity += self.item_quantity
        self.item.save()
        self.item_quantity = 0
        self.save()

    @property
    def price(self):
        return self.item_quantity*self.item.price
    

    # def __str__(self):
    #     return self.customer






    
