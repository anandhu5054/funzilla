import imp
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Address
from store.models import Product
from .models import Cart, CartItem, Coupon, WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


# Create your views here.

# Getting the Cart ID
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# Adding Products to cart
def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)      #getting the product
    # is_wishlisted_product_exists = WishlistItem.objects.filter(product=product,user=current_user).exists()
    # if is_wishlisted_product_exists:
    #     WishlistItem.objects.filter(product=product,user=current_user).delete()
    # If the user is authenticated
    if current_user.is_authenticated:

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            for item in cart_item:
                item.quantity += 1
                item.save()
           
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user =current_user,
            )           
        return redirect('cart')
    # If the user is not authenticated
    else:        
                
        try:                                                        #getting the cart using the cart_id present in the session
            cart = Cart.objects.get(cart_id=_cart_id(request))  
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()


        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            for item in cart_item:
                item.quantity += 1
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            
            cart_item.save()
        return redirect('cart')

    

def remove_cart(request,product_id,cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product,user= request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product,cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request,product_id,cart_item_id):
    product = get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:       
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            a = cart_item.sub_total()
            total += a 
            quantity += cart_item.quantity
        grand_total = total
    except ObjectDoesNotExist:
        pass #just ignore

    if 'coupon_discount' in request.session:
         del request.session['coupon_discount']

    valid_coupon = None
    coupon = None
    invalid_coupon = None
    coupon_discount = 0

    if request.method == "GET":
        coupon_code = request.GET.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code = coupon_code)
                valid_coupon = "Are applicable in Current Order !"
                if (grand_total*coupon.discount/100) < coupon.max_limit:
                    coupon_discount = grand_total*coupon.discount/100
                else:
                    coupon_discount = coupon.max_limit

                grand_total = grand_total - coupon_discount
                request.session['coupon_discount'] = coupon_discount

            except:
                invalid_coupon = "Invalid Coupon Code !"

   
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total': grand_total,
        'coupon' : coupon,
        'valid_coupon' : valid_coupon,
        'invalid_coupon' : invalid_coupon,
        'coupon_discount' : coupon_discount,
    }
    return render(request, 'cart/cart.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):    
    try:       
        
        cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        addresses = Address.objects.filter(user=request.user)
        for cart_item in cart_items:
            a = cart_item.sub_total()
            total += a 
            quantity += cart_item.quantity
        grand_total = total
        coupon_discount = 0
        if 'coupon_discount' in request.session:
            coupon_discount = request.session['coupon_discount']
            grand_total = grand_total - coupon_discount

    except ObjectDoesNotExist:
        pass #just ignore
   
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total': grand_total,
        'coupon_discount' : coupon_discount,
        'addresses' : addresses
    }
    return render(request,'cart/checkout.html', context )


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def add_remove_wishlistItem(request):
    pk = request.GET['id']
    product = Product.objects.get(id=pk)
    is_wishlist_item_exists = WishlistItem.objects.filter(product=product, user=request.user).exists()
    if is_wishlist_item_exists:
        wishlist_item = WishlistItem.objects.get(product=product,user=request.user)
        wishlist_item.delete()
        flag = 1
    else:
        wishlist_item = WishlistItem.objects.create(
                product = product,
                user =request.user,
            )
        flag = 2

    context = {
        'flag':flag
    }
    return JsonResponse(context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def remove_wishlist_item(request,product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    WishlistItem.objects.filter(product=product,user=current_user).delete()
    return redirect('wishlist')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def wishlist(request):
    if request.user.is_authenticated:
        wishlist_items = WishlistItem.objects.filter(user=request.user,is_active=True)
    
    context = {
        'wishlist_items' : wishlist_items,
    }

    return render(request, 'cart/wishlist.html', context)