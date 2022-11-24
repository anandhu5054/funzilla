from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_staff:
            return view_func(request,*args,**kwargs)
        else:
            return redirect('adminSIgnIn')
    return wrapper_func