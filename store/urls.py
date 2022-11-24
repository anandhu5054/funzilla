from django.urls import path 
from . import views


urlpatterns = [
    path('',views.store,name='store'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('category/<slug:category_slug>/',views.store,name='product_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.single_item,name='single_item'),


    path('search/', views.search, name='search'),
] 
