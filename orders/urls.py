from django.urls import path 
from . import views


urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('CashOnDelevery/<str:orderNo>', views.CashOnDelevery, name='CashOnDelevery'),
    path('razorpay_payment_complete/<str:pk>',views.razorpay_payment_complete, name = 'razorpay_payment_complete'),
]