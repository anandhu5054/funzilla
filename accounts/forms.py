
from django import forms
from .models import Account, Address


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name','username', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'

class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')

class AddAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city','postcode']

    def __init__(self, *args, **kwargs):
        super(AddAddressForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'last Name'
        self.fields['phone'].widget.attrs['placeholder'] =  'Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['address_line_1'].widget.attrs['placeholder'] = 'Street address Line 1'
        self.fields['address_line_2'].widget.attrs['placeholder'] = 'Street address Line 2 (Optional)'
        self.fields['country'].widget.attrs['placeholder'] = 'Country'
        self.fields['state'].widget.attrs['placeholder'] = 'State/Division'
        self.fields['city'].widget.attrs['placeholder'] = 'Town/City'
        self.fields['postcode'].widget.attrs['placeholder'] = 'Postcode/ZIP'