from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe


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

    @property
    def add_to_cart(self):
        self.quantity -= 1
        print(f"Added to cart: {self.name}")
        print(self.quantity)

    def __str__(self):
        return self.name





    
