from email.policy import default
from django.urls import reverse
from django.db import models
from category.models import Age, Brand, Charector, Category
import math
from accounts.models import Account
from django.db.models import Avg, Count

class Product(models.Model):
    product_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description1 = models.TextField(max_length=500, blank=True)
    description2  = models.TextField(max_length=500, blank=True)
    stock = models.IntegerField(default=10)
    cost = models.IntegerField(default=10)
    price = models.IntegerField()
    discount=  models.IntegerField(default=0)
    images  = models.ImageField(upload_to='photos/products')
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,null=True)
    age = models.ForeignKey(Age, on_delete=models.CASCADE,null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,null=True, blank=True)
    charector = models.ForeignKey(Charector, on_delete=models.CASCADE,null=True, blank=True)    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date= models.DateTimeField(auto_now=True)


    def discounted_price(self):
        if self.discount is 0:
            return self.price
        else:
            return  math.floor(self.price - (self.discount/100 * self.price))


    def get_url(self):
        return reverse('single_item',args=[self.category.slug,self.slug])

    def __str__(self):
        return self.product_name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class Additional_Information(models.Model):
    product = models.ForeignKey(Product,related_name='additional_information' ,on_delete=models.CASCADE)
    detail1 = models.CharField(max_length=100,default='TEST',null=True, blank=True)
    detail2 = models.CharField(max_length=100,default='TEST',null=True, blank=True)
    detail3 = models.CharField(max_length=100,default='TEST',null=True, blank=True)

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject