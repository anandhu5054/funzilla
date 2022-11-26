from itertools import product
from django.http import HttpResponse
from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages, auth

from cart.models import Cart, CartItem
from .forms import AddAddressForm, RegistrationForm, VerifyForm
from .models import Account, Address
from . import verify
import requests
import re

from cart.views import _cart_id

# Create your views here.

#    USER LOGIN

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        
        if user is not None and user.is_verified:
            try:
                cart= Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item =CartItem.objects.filter(cart=cart)            
                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass

            auth.login(request, user)
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('home')
        else: 
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render(request,'accounts/login.html')

# USER REGISTRATION

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        phone_number = request.POST['phone_number']        
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            username = email.split("@")[0]
            password = form.cleaned_data['password']
            txt = phone_number

            if  txt.isnumeric() and len(txt) == 10:
                phone_number = '+91'+phone_number
                user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password,phone_number=phone_number)
                user.profile_picture = 'default/default-user.png'
                user.save()
                verify.send(phone_number)
                return redirect(f'otp/{user.id}')
            else:
                messages.error(request, 'Please Enter a Valid Mobile Number')
                return redirect('register')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

# USER OTP VALIDATION

def otp(request,id):
    if request.method == 'POST':
        user=Account.objects.get(id=id)
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if verify.check(user.phone_number, code):
                user.is_verified = True
                user.save()
                django_login(request,user)
                messages.success(request, 'Registration Successfull')
                return redirect('home')
    else:
        form = VerifyForm()
    return render(request, 'accounts/otp.html', {'form': form})

#  LOGIN WITH OTP

def login_with_phone(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        phone_number = '+91' +phone_number
        if Account.objects.filter(phone_number=phone_number).exists():
            user = Account.objects.get(phone_number=phone_number)
            verify.send(phone_number)
            return redirect(f'otp_login/{user.id}')
        else:
            messages.success(request, 'Account not found... Please enter registered phone number')

    return render(request,'accounts/phonelogin.html')

def otp_login(request,id):
    if request.method == 'POST':
        user=Account.objects.get(id=id)
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if verify.check(user.phone_number, code):
                django_login(request,user)
                messages.success(request, 'Login Successfull')
                return redirect('home')
    else:
        form = VerifyForm()
    return render(request, 'accounts/otp_login.html', {'form': form})   

#   USER SIGNOUT

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signout(request):
    logout(request)
    return redirect('home')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def add_address(request):
    form = AddAddressForm()
    if request.method == 'POST':
        form = AddAddressForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, 'Address Added Successfull')
            return redirect('checkout') 
    return render(request,'accounts/new_address.html',{'form':form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def add_address_userprofile(request):
    form = AddAddressForm()
    if request.method == 'POST':
        form = AddAddressForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, 'Address Added Successfull')
            return redirect('dashboard') 
    return render(request,'accounts/new_address.html',{'form':form})    