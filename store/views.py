from django.shortcuts import render, get_object_or_404, redirect
from category.models import Category, Age, Brand, Charector
from .models import Additional_Information, Product,ReviewRating, ProductGallery
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator

from orders.models import OrderProduct
from cart.models import CartItem

# Create your views here.

def store(request,category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        is_age_catg_exits = Age.objects.filter(slug=category_slug).exists()
        is_brand_catg_exits = Brand.objects.filter(slug=category_slug).exists()
        is_charector_catg_exits = Charector.objects.filter(slug=category_slug).exists()
        is_main_catg_exits = Category.objects.filter(slug=category_slug).exists()

        if is_main_catg_exits:
            categories = get_object_or_404(Category,slug=category_slug)
            products = Product.objects.filter(Q(category=categories) | Q(category__parent = categories),is_available=True)

        elif is_age_catg_exits:
            ages = get_object_or_404(Age,slug=category_slug)
            products = Product.objects.filter(age=ages,is_available=True)
        
        elif is_brand_catg_exits:
            brands = get_object_or_404(Brand,slug=category_slug)
            products = Product.objects.filter(brand = brands,is_available=True)

        elif is_charector_catg_exits:
            charectors = get_object_or_404(Charector,slug=category_slug)
            products = Product.objects.filter(charector=charectors,is_available=True)
              
        paginator = Paginator(products,9)
        page=request.GET.get('page')
        paged_products = paginator.get_page(page)

    else:
        products = Product.objects.all().filter(is_available=True)
        paginator = Paginator(products,9)
        page=request.GET.get('page')
        paged_products = paginator.get_page(page)
    
    brands = Brand.objects.all()

    context ={ 
        'products' : paged_products,
        'brands' : brands,
    }

    return render(request,'store/store.html',context)


def single_item(request,category_slug,product_slug):
    single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
    product_images = ProductGallery.objects.filter(product=single_product)

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    reviews_countt = ReviewRating.objects.filter(product_id=single_product.id, status=True).count()

    context = {
        'single_product': single_product,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'reviews_countt': reviews_countt,
        'product_images': product_images
    }

    return render(request,'store/singleproduct.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(description1__icontains=keyword) |Q(description2__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)