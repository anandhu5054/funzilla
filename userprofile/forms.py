from django import forms
from accounts.models import Account


class UserForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = Account
        fields = ('first_name', 'last_name','profile_picture')

    # def __init__(self, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'form-control'