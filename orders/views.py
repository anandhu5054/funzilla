from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from cart.models import CartItem
from accounts.models import Address
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        price = item.product.discounted_price()
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.save()

        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock =  product.stock - item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def place_order(request, total=0, quantity=0,):

    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    razorpay_client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        a = cart_item.sub_total()
        total += a 
        quantity += cart_item.quantity
    grand_total = total + tax

    coupon_discount = 0
    if 'coupon_discount' in request.session:
        coupon_discount = request.session['coupon_discount']
        grand_total = grand_total - coupon_discount

    if request.method=='POST':
        if request.POST.get('address') == None:
            messages.error(request, 'Please add an a Address')
            return redirect('checkout')
        else:
            form=OrderForm(request.POST)
            if form.is_valid:
                data = Order()
                data.user = current_user
                some_var = int(request.POST.get('address'))
                data.address = Address.objects.get(id=some_var) 
                data.order_total = grand_total
                data.tax = tax
                data.ip = request.META.get('REMOTE_ADDR')
                data.save()
                # Generate order number
                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr,mt,dt)
                current_date = d.strftime("%Y%m%d") #20210305
                order_number = current_date + str(data.id)
                data.order_number = order_number
                data.save()
                order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

                price = data.order_total * 100
                razor_payment = razorpay_client.order.create(
                    {"amount": int(price),
                    "currency": "INR", 
                })

                context = {
                    'order': order,
                    'cart_items': cart_items,
                    'total': total,
                    'grand_total': grand_total,
                    'coupon_discount' : coupon_discount,
                    "raz_payment": razor_payment
                }
                return render(request, 'cart/place_order.html', context)
    else:
        return redirect('checkout')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def razorpay_payment_complete(request, pk):
    body = json.loads(request.body)
    razorpay_client = razorpay.Client(
        auth=(str(settings.RAZORPAY_KEY_ID), str(settings.RAZORPAY_KEY_SECRET))
    )
    razorpay_client.set_app_details({"title": "Funzilla", "version": "1.1v"})
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=pk)
    ''
    try:
        razorpay_client.utility.verify_payment_signature(body)
        payment = Payment(
            user = request.user,
            payment_id = body['razorpay_payment_id'],
            payment_method = 'Razorpar',
            amount_paid = order.order_total,
            status = 'Completed',
        )
        payment.save()

        order.payment = payment
        order.is_ordered = True
        order.save()

        # Move the cart items to Order Product table
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            price = item.product.discounted_price()
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = price
            orderproduct.ordered = True
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.save()

            # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock =  product.stock - item.quantity
            product.save()

            # Clear cart
            CartItem.objects.filter(user=request.user).delete()


            data = {
                'order_number': order.order_number,
                'transID': payment.payment_id,
            }
        return JsonResponse(data)
    except:
        raise Exception("internal errors")




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def CashOnDelevery(request,orderNo):
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=orderNo)

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        price = item.product.discounted_price()
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.save()

        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock =  product.stock - item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()


    try:
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        coupon_discount = 0
        if 'coupon_discount' in request.session:
            coupon_discount = request.session['coupon_discount']

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'coupon_discount' : coupon_discount,
            'subtotal': subtotal,
        }
        return render(request, 'cart/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
 
 
 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        coupon_discount = 0
        if 'coupon_discount' in request.session:
            coupon_discount = request.session['coupon_discount']

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'coupon_discount' : coupon_discount,
            'subtotal': subtotal,
        }
        return render(request, 'cart/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
 
 
 
 
 
 
 
 
 
 
 
