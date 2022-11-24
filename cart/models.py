from django.db import models
from store.models import Product
from accounts.models import Account
import math

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='cart_item')
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        discounted_price = self.product.discounted_price()
        return  discounted_price * self.quantity

    def _str_(self):
        return self.Product

class Coupon(models.Model):
    code = models.CharField(max_length=200,blank=True)
    discount = models.IntegerField()
    max_limit = models.IntegerField()
    
    def _str_(self):
        return self.code


class WishlistItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='WishlistItem')
    is_active = models.BooleanField(default=True)

    def _str_(self):
        return self.Product