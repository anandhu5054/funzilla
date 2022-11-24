from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.forms.models import inlineformset_factory
from accounts.models import Account
from store.models import Additional_Information, Product
from category.models import Category, Charector, Brand, Age
from .forms import ProductDetailsForm ,OrderedProductForm, AddCouponForm,DiscountForm , AddAgeForm,AddBrandForm,AddCategoryForm,AddCharectorForm
from .decorators import unauthenticated_user
from django.views.decorators.cache import cache_control
from orders.models import OrderProduct
from cart.models import Coupon
from django.http import HttpResponse
from django.utils.text import slugify

from datetime import datetime
from .helpers import save_pdf

# Create your views here.

# admin signin
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminSIgnIn(request):
    if request.user.is_staff:
        return redirect('adminhome')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('adminhome')
        else: 
            messages.error(request, 'Invalid Credentials')
            return redirect('adminSIgnIn')
    else:
        return render(request, 'adminpanel/adminsignin.html')

def adminlogout(request):
    logout(request)
    return redirect('adminSIgnIn')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@unauthenticated_user
def adminhome(request):

    total_sold_products = OrderProduct.objects.filter(ordered=True)
    profit = 0
    sales = OrderProduct.objects.filter(ordered=True).count() 
    users = Account.objects.filter(is_active=True).count() 
    products = Product.objects.filter(is_available=True).count()

    for items in total_sold_products:
        profit += items.product.price- items.product.cost


    labels=[]
    data=[]

    New=0
    Accepted=0
    Completed=0
    Cancelled=0

    queryset= OrderProduct.objects.all().order_by('-created_at')
    for product in queryset:
        if product.status == 'New':
            New+=1
        elif product.status == 'Accepted':
            Accepted+=1
        elif product.status == 'Completed':
            Completed+=1
        else:
            Cancelled+=1

    labels=["New","Accepted","Completed","Cancelled"]
    data=[New,Accepted,Completed,Cancelled]


    # breakpoint()
    # from django.db.models.functions import TruncMonth
    # OrderProduct.objects.annotate(month=TruncMonth('timestamp')).values('month').annotate(c=Count('id')).values('month', 'c')     # Truncate to month and add to select list
    #                              # Group By month
    #                  # Select the count of the grouping
     
    context = {
        'total_sold_products' : total_sold_products,
        'profit' : profit,
        'sales' : sales,
        'users' : users,
        'products' : products,
        'data':data,
        'labels':labels
    }
    return render(request,'adminpanel/adminhome.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@unauthenticated_user
# User Management
def usersmanagement(request,pk=None):
    form = Account.objects.filter(is_staff = False)
    if pk != None:
        user = Account.objects.get(id=pk)
        if user.is_active:                          # Deactivating User
            user.is_active = False
            user.save()
            return redirect(usersmanagement)
        else:
            user.is_active = True                   # Activating User
            user.save()    
            return redirect(usersmanagement)
    return render(request,'adminpanel/usersmanagement.html',{'form':form})

# Product Display
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@unauthenticated_user
def productmanagement(request,pk=None):
    products = Product.objects.all()
    if pk != None:
        product = Product.objects.get(id=pk)
        if product.is_available:
            product.is_available = False
            product.save()
            return redirect(productmanagement)
        else:
            product.is_available = True
            product.save()    
            return redirect(productmanagement)
    return render(request,'adminpanel/productmanagement.html',{'products':products})

# Product Details and Product Update
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@unauthenticated_user
def productmanagement_details(request,pk):
    product = Product.objects.get(id=pk)
    productDetails_form = ProductDetailsForm(request.POST,request.FILES,instance=product)
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        stock = request.POST.get('stock')
        cost = request.POST.get('cost')
        price = request.POST.get('price')
        detail1 = request.POST.get('detail1')
        detail2 = request.POST.get('detail2')
        detail3 = request.POST.get('detail3')
        if productDetails_form.is_valid():
            productDetails_form.save()
            messages.success(request, 'Product Updated Successfully')
    else:    
        productDetails_form = ProductDetailsForm(instance=product)
    context ={
        'productDetails_form':productDetails_form,
    }
    return render(request,'adminpanel/product_details.html',context)

def add_product(request):
    
    if request.method == 'POST':
        productDetails_form = ProductDetailsForm(request.POST,request.FILES)
        if productDetails_form.is_valid():
            post = productDetails_form.save(commit=False)
            post.slug = slugify(post.product_name)
            post.save()

            messages.success(request, 'Product Added Successfully')
    else:    
        productDetails_form = ProductDetailsForm()
    context ={
        'productDetails_form':productDetails_form,
    }
    return render(request,'adminpanel/add_product.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@unauthenticated_user
def ordermanagement(request):
    ordered_products = OrderProduct.objects.filter(ordered=True).order_by('-created_at')
    context = {
        'ordered_products' : ordered_products
    }
    return render(request,'adminpanel/ordermanagement.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@unauthenticated_user
def orderstatusUpdation(request,pk):
    oredered_product = OrderProduct.objects.get(id=pk)
    orderstatusUpdationForm = OrderedProductForm(request.POST,instance=oredered_product)
    price = oredered_product.product_price * oredered_product.quantity
    
    if request.method == 'POST':
        if orderstatusUpdationForm.is_valid:
            if orderstatusUpdationForm['status'].value() == 'Cancelled' or orderstatusUpdationForm['status'].value() == 'Returned':
                # breakpoint()
                oredered_product.product.stock += 1
                oredered_product.product.save()

            orderstatusUpdationForm.save()
            messages.success(request, 'Order Updated Successfully')
    context = {
        'oredered_product' : oredered_product,
        'orderstatusUpdationForm' : orderstatusUpdationForm,
        'price' : price        
    }    
    return render(request, 'adminpanel/orderupdation.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@unauthenticated_user
def sales_report(request):
    ordered_products = OrderProduct.objects.filter(ordered=True)
    context = {
        'ordered_products' : ordered_products
    }

    pdf = save_pdf('adminpanel/sales_report.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

    # file_name, status = save_pdf(context)

    # return Response{{'status' : 200, 'path' : f'/media/{file_name}.pdf'}}

    # return render(request,'adminpanel/sales_report.html',context)

def coupon_offer(request):
    coupons = Coupon.objects.all()
    discounted_products = Product.objects.filter(discount__gt =1)
    context = {
        'coupons' : coupons,
        'discounted_products':discounted_products
    }
    return render(request, 'adminpanel/admin_coupon_offer.html',context)

def add_coupon(request):
    if request.method =='POST':
        form = AddCouponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coupon Added Successfully')
            return redirect('coupon_offer')
    form = AddCouponForm()
    context = {
        'form':form
    }
    return render(request, 'adminpanel/add_coupon.html',context)

def delete_coupon(request,pk):
    Coupon.objects.get(id=pk).delete()
    messages.success(request,'Coupon Deleted')
    return redirect('coupon_offer')

def add_discount(request):
    products = Product.objects.filter(is_available=True)

    if request.method =='POST':
        product_namee = request.POST.get('product_name')
        discount = request.POST.get('discount')
        breakpoint()
        product = Product.objects.get(product_name=product_namee,is_available=True)
        product.discount=discount
        product.save()
        messages.success(request, 'Discount Added Successfully')
        return redirect('coupon_offer')


    context = {
        'products':products,
    }
    return render(request, 'adminpanel/add_discount.html',context)

def delete_discount(request,pk):
    discounted_product  = Product.objects.get(id=pk)
    discounted_product.discount=0
    discounted_product.save()
    messages.success(request,'Discount Canceled')
    return redirect('coupon_offer')

######### CATEGORIES #########


def categories(request):
    main_category = Category.objects.all()
    age_category = Age.objects.all()
    brands = Brand.objects.all()
    charectors = Charector.objects.all()

    context = {
        'main_category' : main_category,
        'age_category' : age_category,
        'brands' : brands,
        'charectors':charectors
    }
    return render(request,'adminpanel/admin_categories.html',context)


def add_category(request):
    if request.method =='POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.category_name)
            post.save()
            messages.success(request,'Category Added')
            return redirect('categories')
    form = AddCategoryForm()
    context = {
        'form':form
    }

    return render(request,'adminpanel/add_category.html',context)

def delete_category(request,pk):
    Category.objects.get(id=pk).delete()
    messages.success(request,'Category Deleted')
    return redirect('categories')


def add_brand(request):
    if request.method =='POST':
        form = AddBrandForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.brand_name)
            post.save()
            messages.success(request,'Brand Added')
            return redirect('categories')
    form = AddBrandForm()
    context = {
        'form':form
    }

    return render(request,'adminpanel/add_brand.html',context)

def delete_brand(request,pk):
    Brand.objects.get(id=pk).delete()
    messages.success(request,'Brand Deleted')
    return redirect('categories')

def add_charector(request):
    if request.method =='POST':
        form = AddCharectorForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.charector_name)
            post.save()
            messages.success(request,'Charector Added')
            return redirect('categories')
    form = AddCharectorForm()
    context = {
        'form':form
    }
    return render(request,'adminpanel/add_charector.html',context)

def delete_charector(request,pk):
    Charector.objects.get(id=pk).delete()
    messages.success(request,'Charector Deleted')
    return redirect('categories')

def add_agecat(request):
    if request.method =='POST':
        form = AddAgeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.age_name)
            post.save()
            messages.success(request,'Age Category Added')
            return redirect('categories')
    form = AddAgeForm()
    context = {
        'form':form
    }
    return render(request,'adminpanel/add_agecat.html',context)

def delete_agecat(request,pk):
    Age.objects.get(id=pk).delete()
    messages.success(request,'Age Category Deleted')
    return redirect('categories')