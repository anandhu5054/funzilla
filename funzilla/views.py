from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render
from category.models import Category,Age,Charector,Brand
from store.models import Product




def home(request):


    featured_products = Product.objects.filter(is_featured=True,is_available=True)
    new_products =  Product.objects.filter(is_available=True).order_by('-modified_date')[:3]
    sale_products = Product.objects.filter(is_available=True,discount__gt = 1)

    age = Age.objects.all().order_by('-id')
    charector = Charector.objects.all().order_by('-id')
    brand = Brand.objects.all().order_by('-id')
    context={
        'featured_products':featured_products,
        'new_products' :new_products,
        'sale_products':sale_products,
        'age':age,
        'charector':charector,
        'brand':brand
    }
    return render(request, 'home.html',context)