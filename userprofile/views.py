from django.shortcuts import render, redirect
from orders.models import OrderProduct, Order
from accounts.models import Address
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from django.contrib import messages
from accounts.models import Account

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def dashboard(request):
    
    user = request.user
    address = Address.objects.filter(user=request.user)

    context={
        'address' : address,
        'user' : user
    }
    return render(request,'userprofile/dashboard.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def dashboard_orders(request):
    ordered_products = OrderProduct.objects.filter(user=request.user,ordered=True).order_by('-created_at')
    price=0
    for product in  ordered_products:
        price = product.quantity * product.product_price
    
    context={
        'ordered_products' : ordered_products,
        'price' : price,
    }
    return render(request,'userprofile/dashboard_orders.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def dashboard_adress(request):
    
    user = request.user
    address = Address.objects.filter(user=request.user)

    context={
        'address' : address,
        'user' : user
    }
    return render(request,'userprofile/dashboard_adress.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def dashboard_accounts(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST,request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('dashboard')
    else:
        user_form = UserForm(instance=request.user)
    context = {
        'user_form': user_form,
    }
    return render(request,'userprofile/dashboard_accounts.html',context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('dashboard_accounts')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('dashboard_accounts')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('dashboard_accounts')
    return render(request, 'userprofile/dashboard_accounts.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def cancel_order(request,pk):
    ordered_product = OrderProduct.objects.get(id=pk)
    ordered_product.product.stock += 1
    ordered_product.product.save()
    ordered_product.status = "Cancelled"
    ordered_product.save()
    return redirect('dashboard_orders')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def return_product(request,pk):
    ordered_product = OrderProduct.objects.get(id=pk)
    ordered_product.product.stock += 1
    ordered_product.product.save()
    ordered_product.status = "Return Initiated"
    ordered_product.save()
    return redirect('dashboard_orders')