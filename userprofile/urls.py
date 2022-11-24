from django.urls import path
from userprofile import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('dashboard_orders',views.dashboard_orders,name='dashboard_orders'),
    path('dashboard_adress',views.dashboard_adress,name='dashboard_adress'),
    path('dashboard_accounts',views.dashboard_accounts,name='dashboard_accounts'),
    path('change_password',views.change_password,name='change_password'),
    path('cancel_order/<int:pk>',views.cancel_order,name='cancel_order'),
    path('return_product',views.return_product,name='return_product')
]