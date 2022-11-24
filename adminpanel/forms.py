from django import forms
from store.models import Product
from orders.models import OrderProduct
from cart.models import Coupon
from category.models import Category,Age,Brand,Charector

class ProductDetailsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','stock','cost','price','images','is_available','is_featured','category','age','brand','charector','description1','description2']


class OrderedProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['status']

class AddCouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code','discount','max_limit']

class DiscountForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'discount']


###### CATEGORY FORMS 

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']

class AddBrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name']

class AddAgeForm(forms.ModelForm):
    class Meta:
        model = Age
        fields = ['age_name']

class AddCharectorForm(forms.ModelForm):
    class Meta:
        model = Charector
        fields = ['charector_name']
