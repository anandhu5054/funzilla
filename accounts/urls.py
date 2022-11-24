from django.contrib import admin
from django.urls import path 
from . import views


urlpatterns = [
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('otp/<str:id>',views.otp,name='otp'),
    path('login_with_phone',views.login_with_phone,name='login_with_phone'),
    path('otp_login/<str:id>',views.otp_login,name='otp_login'),
    path('signout',views.signout,name='signout'),
    path('add_address',views.add_address,name='add_address'),
    
    path('add_address_userprofile',views.add_address_userprofile,name='add_address_userprofile'),
] 
