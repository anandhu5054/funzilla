from django.contrib import admin
from django.urls import path 
from . import views


urlpatterns = [
    path('',views.adminhome,name='adminhome'),
    path('adminSIgnIn',views.adminSIgnIn,name='adminSIgnIn'),
    path('usersmanagement',views.usersmanagement,name='usersmanagement'),
    path('usersmanagement/<str:pk>',views.usersmanagement,name='usersmanagement'),
    path('productmanagement',views.productmanagement,name='productmanagement'),
    path('add_product',views.add_product,name='add_product'),
    path('productmanagement/<str:pk>',views.productmanagement,name='productmanagement'),
    path('productmanagement_details/<str:pk>',views.productmanagement_details,name='productmanagement_details'),
    path('ordermanagement',views.ordermanagement,name='ordermanagement'),
    path('orderstatusUpdation/<str:pk>',views.orderstatusUpdation,name='orderstatusUpdation'),

    path('sales_report',views.sales_report,name='sales_report'),

    path('coupon_offer',views.coupon_offer,name='coupon_offer'),
    path('add_coupon',views.add_coupon,name='add_coupon'),
    path('delete_coupon/<str:pk>',views.delete_coupon,name='delete_coupon'),
    path('add_discount',views.add_discount,name='add_discount'),
    path('delete_discount/<str:pk>',views.delete_discount,name='delete_discount'),

    path('categories',views.categories,name='categories'),

    path('add_category',views.add_category,name='add_category'),
    path('delete_category/<str:pk>',views.delete_category,name='delete_category'),

    path('add_brand',views.add_brand,name='add_brand'),
    path('delete_brand/<str:pk>',views.delete_brand,name='delete_brand'),

    path('add_charector',views.add_charector,name='add_charector'),
    path('delete_charector/<str:pk>',views.delete_charector,name='delete_charector'),

    path('add_agecat',views.add_agecat,name='add_agecat'),
    path('delete_agecat/<str:pk>',views.delete_agecat,name='delete_agecat'),

    

    path('adminlogout',views.adminlogout,name='adminlogout'),
    

] 
