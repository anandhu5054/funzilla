from django.db import models
from accounts.models import Account, Address
from store.models import Product, Variation



class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100) # this is the total amount paid
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    order_total = models.FloatField()
    tax = models.FloatField()
    
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # def __str__(self):
    #     return self.address.first_name


class OrderProduct(models.Model):
    STATUS = (
        ('Placed', 'Placed'),
        ('Accepted', 'Accepted'),
        ('Shiped', 'Shiped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Return Initiated', 'Return Initiated'),
        ('Returned', 'Returned'),
        ('Cancelled', 'Cancelled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE,blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Placed')
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
