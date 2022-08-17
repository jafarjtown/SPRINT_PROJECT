
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from administrator.views import Category
from decorators import is_logged_in, kitchen_only
# from administrator.views import Category
from . import models

# Create your views here.

#TODO: Active Orders page (confirm/decline)
#TODO: Dashboard
#TODO: Login
#TODO: News
#TODO: Customer Orders

@kitchen_only
def Orders(request):
    ord = list()
    orders = models.Order.objects.all()
    kitchen = models.Kitchen.objects.all()[0]
    
    for order in orders:
        for o in order.items.all():
            ord.append(o)
    # print(request.user)
    return render(request, 'kitchen/orders.html', {'orders': ord, 'kitchen':kitchen})

@kitchen_only
def ActiveOrders(request):
    context = {
        "object": models.Order.objects.filter(is_delivered=False),
        "kitchen": models.Kitchen.objects.all()[0]
    }
    return render(request, 'kitchen_active_orders.html',context)

@kitchen_only
def Dashboard(request):
    context = {
        "orders": models.Ordered.objects.all(),
        "user": request.user,
        "kitchen": models.Kitchen.objects.all()[0]
    }
    return render(request, 'kitchen/kitchen_dashboard.html', context)

@kitchen_only
def CustomerOrders(request):
    context = {
        "object": models.Ordered.objects.all()
    }
    return render(request, 'kitchen_customer_view.html', context)

@kitchen_only
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
        "categories": models.Category.objects.all(),
        "kitchen": models.Kitchen.objects.all()[0]
    }
    return render(request, 'kitchen/add_food.html', context)

@kitchen_only
def Manage_Food(request):
    foods = models.Food.objects.all()
    kitchen = models.Kitchen.objects.all()[0]

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
    return render(request, 'kitchen/foods.html', {'foods': foods, 'kitchen':kitchen})

@kitchen_only
def OrderConfirm(request, order_id):
    order = models.Ordered.objects.get(id=order_id)
    order.status = 'D'
    order.save()
    messages.info(request,'Order Status Changed to Delivered')
    return redirect('kitchen:orders')

@kitchen_only
def OrderDecline(request, order_id):
    order = models.Ordered.objects.get(id=order_id)
    order.status = 'R'
    order.save()
    messages.info(request,'Order Status Changed to Rejected')
    return redirect('kitchen:orders')

@kitchen_only
def NotAvailable(request):
    foods = models.Food.objects.filter(quantity__lte=1)
    kitchen = models.Kitchen.objects.all()[0]
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
    return render(request, 'kitchen/not-available.html', {'foods': foods, 'kitchen':kitchen})