
from django.shortcuts import redirect, render
from django.contrib.messages import add_message, constants
from authentication.models import User
from django.contrib.auth import login, logout,authenticate

from decorators import is_logged_in
# Create your views here.


def LogOut(request):
    logout(request)
    return redirect('restaurant:welcome')

@is_logged_in
def Login(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            add_message(request, constants.SUCCESS, 'login success')
            if user.is_kitchen: return redirect('kitchen:dashboard')
            elif user.is_admin: return redirect('administrator:dashboard')
            return redirect('restaurant:dashboard')
        add_message(request, constants.ERROR, 'Invalid credentials')
    return render(request, 'authentication/login.html')

@is_logged_in
def Register(request):
    if request.method == 'POST':
        p1 = request.POST.get('p1')
        p2 = request.POST.get('p2')
        if p1 != p2:
            add_message(request, constants.ERROR, 'Password(s) din\'t match ')
        else:
            if User.objects.filter(username = request.POST.get('username')).exists():
                add_message(request, constants.ERROR, 'Username is not available')
            elif User.objects.filter(email = request.POST.get('email')).exists():
                add_message(request, constants.ERROR, 'Email address in use')
            else:
                u = request.POST.get('username')
                dob = request.POST.get('date of birth')
                f = request.POST.get('first name')
                l = request.POST.get('last name')
                e = request.POST.get('email')
                ph = request.POST.get('phone number')
                id = request.POST.get('account_id')
                ty = request.POST.get('account_type')
                user = User.objects.create_user(username=u,first_name=f,last_name=l,email=e,account_id=id,account_type=ty, date_of_birth=dob, phone_no=ph, password=p1)
                add_message(request, constants.SUCCESS, 'Account created')
                login(request, user)
                return redirect('restaurant:dashboard')
                
    return render(request, 'authentication/signin.html')