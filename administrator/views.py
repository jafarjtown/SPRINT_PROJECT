from django.shortcuts import redirect, render
from django.db.models import Q

from administrator.forms import BlogForm
from administrator.models import Blog, RestaurantService
from authentication.models import User
from decorators import administrator_only
from kitchen.models import Kitchen

# Create your views here.


@administrator_only
def Dashboard(request):
    return render(request, 'administrator/dashboard.html')

@administrator_only
def Profile(request):
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
def Kitchens(request):
    user = request.user
    kitchens = user.restaurant.kitchens.all()
    return render(request, 'administrator/kitchens.html', {'kitchens':kitchens})

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
def KitchenView(request, kitchen_id):
    kitchen = Kitchen.objects.get(id = kitchen_id)
    users = User.objects.filter(is_admin=False,is_kitchen=False)
    return render(request, 'administrator/kitchen.html', {'kitchen':kitchen, 'users':users})


@administrator_only
def AssignKitchenAttendant(request,kitchen_id):
    user = request.user
    try:
        attendant = User.objects.get(username=request.POST.get('user'))
        kitchen = user.restaurant.kitchens.get(id = kitchen_id)
        kitchen.attendant = attendant
        kitchen.save()
        attendant.is_kitchen = True
        attendant.save()
        return redirect(kitchen.get_absolute_url())
    except Exception as e:
        print(e)
        return redirect('restaurant:welcome')
        
@administrator_only
def KitchenOrders(request, kitchen_id):
    user = request.user
    kitchen = user.restaurant.kitchens.get(id=kitchen_id)
    orders = kitchen.ordered.all()
    return render(request, 'administrator/orders.html', {'orders': orders}) 


@administrator_only
def KitchenOrdersSummary(request, kitchen_id):
    user = request.user
    kitchen = user.restaurant.kitchens.get(id=kitchen_id)
    summary = kitchen.orders_sum
    print(summary)
    return render(request, 'administrator/order-summary.html', {'summary': summary}) 