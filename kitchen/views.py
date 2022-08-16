
from django.shortcuts import render

from administrator.views import Category

# from administrator.views import Category
from . import models

# Create your views here.

#TODO: Active Orders page (confirm/decline)
#TODO: Dashboard
#TODO: Login
#TODO: News
#TODO: Customer Orders


def Orders(request):
    ord = list()
    orders = models.Order.objects.all()
    for order in orders:
        for o in order.items.all():
            ord.append(o)
    # print(request.user)
    return render(request, 'kitchen/orders.html', {'orders': ord})


def ActiveOrders(request):
    context = {
        "object": models.Order.objects.filter(is_delivered=False)
    }
    return render(request, 'kitchen_active_orders.html',context)
def Dashboard(request):
    context = {
        "orders": models.Ordered.objects.all(),
        "user": request.user
    }
    return render(request, 'kitchen/kitchen_dashboard.html', context)
def Login(request):
    pass
def News(request):
    context = {
        "object": models.News.objects.all()
    }
    return render(request, 'news_page.html', context)
def CustomerOrders(request):
    context = {
        "object": models.Ordered.objects.all()
    }
    return render(request, 'kitchen_customer_view.html', context)
def Add_food(request):
    if request.POST:
        food = models.Food()
        food.name = request.POST.get('name')
        food.price = request.POST.get('price')
        food.quantity = request.POST.get('quantity')
        food.image = request.FILES.get('image')
        food.category = models.Category.objects.get(name = request.POST.get('category'))
        food.save()
    context = {
        "categories": models.Category.objects.all()
    }
    return render(request, 'kitchen/add_food.html', context)

def Manage_Food(request):
    foods = models.Food.objects.all()
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        food = request.POST.get('food')
        f = models.Food.objects.get(id = food[0])
        f.quantity = quantity
        f.name = name
        f.price = price
        f.save()
        print(f)
    return render(request, 'kitchen/foods.html', {'foods': foods})
