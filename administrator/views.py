from django.shortcuts import redirect, render
from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist

from administrator.forms import BlogForm
from administrator.models import Blog, RestaurantService
from authentication.models import User
from decorators import administrator_only, is_logged_in
from django.contrib.messages import add_message, constants
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.hashers import check_password,  make_password
from kitchen.models import Kitchen, Ordered

# Create your views here.


@administrator_only
def Dashboard(request):
    return render(request, 'administrator/dashboard.html')

@administrator_only
def Profile(request):
    return render(request, 'administrator/profile-view.html')

@administrator_only
def UpdateProfile(request):
    return render(request, 'administrator/profile.html')


@administrator_only
def Blogs(request):
    blogs = request.user.posts.all()
    return render(request, 'administrator/posts.html', {'posts': blogs})
@administrator_only
def NewBlog(request):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
    return render(request, 'administrator/new-post.html', {'form': form})

@administrator_only
def UpdateBlog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    form = BlogForm(instance=blog)
    if request.method == 'DELET':
        blog.delete()
        return redirect('administrator:posts')
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
    return render(request, 'administrator/new-post.html', {'form': form})

@administrator_only
def NotAvailable(request):
    foods = request.user.restaurant.not_available_foods
    return render(request, 'administrator/not-available.html', {'foods': foods})
@administrator_only
def Orders(request):
    user = request.user
    orders = []
    restaurant = user.restaurant
    orders.extend(restaurant.orders)
    return render(request, 'administrator/orders.html', {'orders': orders})

@administrator_only
def StudentCustomers(request):
    user = request.user
    customers = set()
    restaurant = user.restaurant
    for ord in restaurant.orders:
        print(ord)
        customers.add(ord.customer)
    return render(request, 'administrator/customers.html', {'customers':customers})

@administrator_only
def OrderSummary(request):
    user = request.user
    orders = []
    restaurant = user.restaurant
    orders.extend(restaurant.orders_sum)
    return render(request, 'administrator/order-summary.html', {'summary': orders})


@administrator_only
def Foods(request):
    user = request.user
    foods = user.restaurant.foods
    return render(request, 'administrator/foods.html', {'foods': foods})


@administrator_only
def NewRestaurant(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        phone_no = data.get('phone_no')
        address = data.get('address')
        rest = RestaurantService.objects.create(admin=request.user, name=name, address=address,phone_no=phone_no)
        return redirect('administrator:dashboard')
    return render(request, 'administrator/new-restaurant.html')

# !! YOU CAN'T CREATE MORE THAN ONE KITCHEN
@administrator_only
def NewKitchen(request):
    if request.method == 'POST':
        user = request.user
        data = request.POST
        name = data.get('name')
        phone_no = data.get('phone_no')
        address = data.get('address')
        image = request.FILES.get('image')
        kitchen = Kitchen.objects.create(image=image, name=name, address=address,phone_number=phone_no)
        user.restaurant.kitchens.add(kitchen)
        user.restaurant.save()
        return redirect('administrator:kitchens')
    return render(request, 'administrator/new-kitchen.html')


@administrator_only
def KitchenView(request):
    user = request.user
    kitchen = user.restaurant.kitchen
    users = User.objects.filter(is_admin=False,is_kitchen=False)
    return render(request, 'administrator/kitchen.html', {'kitchen':kitchen, 'users':users})


@administrator_only
def AssignKitchenAttendant(request):
    user = request.user
    if request.method == 'POST':
        kitchen = user.restaurant.kitchen
        try:
            u = request.POST.get('username')
            dob = request.POST.get('date of birth')
            f,l =  request.POST.get('full name').split(' ')
            # f = request.POST.get('first name')
            # l = request.POST.get('last name')
            e = request.POST.get('email')
            ph = request.POST.get('phone number')
            id = request.POST.get('account_id')
            ty = request.POST.get('account_type')
            p1 = request.POST.get('password')
            attendant = User.objects.create_user(username=u,first_name=f,last_name=l,email=e,account_id=id,account_type=ty, date_of_birth=dob, phone_no=ph, password=p1)
            kitchen = user.restaurant.kitchen
            kitchen.attendants.add(attendant)
            kitchen.save()
            attendant.is_kitchen = True
            attendant.save()
            # return redirect(kitchen.get_absolute_url())
        except Exception as e:
            print(e)
            return redirect('administrator:dashboard')
    return render(request, 'administrator/new-kitchen-attendant.html')
        
@administrator_only
def KitchenOrders(request):
    user = request.user
    kitchen = user.restaurant.kitchen
    orders = kitchen.ordered.all()
    return render(request, 'administrator/orders.html', {'orders': orders}) 

@administrator_only
def KitchenOrdersSummary(request):
    user = request.user
    kitchen = user.restaurant.kitchen
    summary = kitchen.orders_sum
    print(summary)
    return render(request, 'administrator/order-summary.html', {'summary': summary}) 

def CustomerProfile(request, username):
    customer = User.objects.get(username = username)
    return render(request, 'administrator/customer-profile.html', {'customer': customer})


def DeclinedOrder(request, order_id):
    ordered = Ordered.objects.get(id = order_id)
    try:
        order = ordered.kitchen.foods.get(name = ordered.name)
        order.quantity = F('quantity') + ordered.quantity
        order.save()
        ordered.delete()
    except ObjectDoesNotExist:
        ordered.delete()
    return redirect('administrator:orders')

def Category(request):
    return render(request, 'administrator/category.html')

def AddFood(request):
    return render(request, 'administrator/add-food.html')
@administrator_only
def ChangePassword(request):
    if request.method == 'POST':
        user = request.user
        current_password = request.POST.get('current password')
        new_password = request.POST.get('new password')
        confirm_password = request.POST.get('confirm password')
        if check_password(current_password, user.password):
            if new_password  == confirm_password:
                user.password = make_password(confirm_password)
                user.save()
                return redirect('administrator:dashboard')
            else:
                add_message(request, constants.ERROR, 'Passwords didnt match')
                
        else:
            add_message(request, constants.ERROR, 'Password is Incorrect')
    return render(request, 'administrator/change-password.html')
@is_logged_in
def AdminLogin(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            if user.is_admin == False:
                add_message(request, constants.ERROR, 'This is Account didnt have access to administrator dashboard')
                return redirect('administrator:login')
            login(request, user)
            add_message(request, constants.SUCCESS, 'login success')
            if user.is_kitchen: return redirect('kitchen:dashboard')
            elif user.is_admin: return redirect('administrator:dashboard')
            return redirect('restaurant:dashboard')
        add_message(request, constants.ERROR, 'Invalid credentials')
    return render(request, 'administrator/login.html')