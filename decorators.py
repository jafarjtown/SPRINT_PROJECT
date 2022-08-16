

from functools import wraps

from django.shortcuts import redirect


def is_logged_in(func):
    @wraps(func)
    def wrap(request,*args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if user.is_admin or user.is_kitchen:
                return redirect('administrator:dashboard')
            elif user.is_kitchen:
                return redirect('kitchen:dashboard')
            return redirect('restaurant:dashboard')
        else:
            return func(request, *args, **kwargs)
    return wrap

def administrator_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if user.is_admin: 
                return function(request, *args, **kwargs)
            else:
                return redirect('restaurant:welcome')
        else:
            return redirect('administrator:login')
    return wrap

def kitchen_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_kitchen:
            return function(request, *args, **kwargs)
        else:
            return redirect('restaurant:welcome')
    return wrap


def customer_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_admin:
            return redirect('administrator:dashboard')
        elif user.is_kitchen:
            return redirect('kitchen:dashboard')
        else:
            return function(request, *args, **kwargs)
    return wrap