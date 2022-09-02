
from datetime import date
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.db.models import Q,F
from decorators import is_logged_in, kitchen_only
from administrator.models import Message
from administrator.views import get_this_week_sells, get_total_sells
# from administrator.views import Category
from . import models

# Create your views here.

#TODO: Active Orders page (confirm/decline)
#TODO: Dashboard
#TODO: Login
#TODO: News
#TODO: Customer Orders

def initiate_restaurant_kitchen(request):
    user = request.user
    kitchen = models.Kitchen.objects.select_related().filter(attendants=request.user)[0]
    restaurant = kitchen.restaurant_kitchen
    return restaurant, kitchen

def get_active_orders(kitchen):
    all = kitchen.ordered_set.filter(status = 'P')
    return all


@login_required
@kitchen_only
def StemChat(request):
    restaurant, kitchen = initiate_restaurant_kitchen(request) 
    if request.method == 'POST':
        import datetime
        user = request.user.username
        text = request.POST.get('text')
        message  = Message()
        message.sender = user
        message.text = text
        message.timestamp = datetime.datetime.now()
        if request.FILES.get('file') != None:
            message.attached_file = request.FILES.get('file')
        message.save()
        restaurant.staff_chat.add(message)
        return redirect('kitchen:chat')
    messages = restaurant.staff_chat.all()
    return render(request, 'kitchen/stemchat.html', {'msgs':messages})

@login_required
@kitchen_only
def FoodifyChat(request):
    restaurant, kitchen = initiate_restaurant_kitchen(request) 
    if request.method == 'POST':
        import datetime
        user = request.user.username
        text = request.POST.get('text')
        message  = Message()
        message.sender = user
        message.text = text
        message.timestamp = datetime.datetime.now()
        if request.FILES.get('file') != None:
            message.attached_file = request.FILES.get('file')
        message.save()
        restaurant.foodify_chat.add(message)
        return redirect('kitchen:chat')
    messages = restaurant.foodify_chat.all()
    return render(request, 'kitchen/stemchat.html', {'msgs':messages})

@login_required
@kitchen_only
def Orders(request):
    # ord = list()
    kitchen_instance = models.Kitchen.objects.select_related().filter(attendants=request.user)[0]
    # try:
        # orders = request.user.attendants.get(username=)
    # .....
    # lets get the ordered item all at once without
    # looping through Orders
    orders = models.Ordered.objects.select_related().filter(kitchen=kitchen_instance)
    # this is same as
    # here we elimate the use of for loop and the databse query
    # ......
    
    # ......
    # this
    # orders = models.Order.objects.all()
    # for order in orders:
    #     for o in order.items.all():
    #         ord.append(o)
    # .......
    return render(request, 'kitchen/orders.html', {'orders': orders, 'kitchen':kitchen_instance})

@login_required
@kitchen_only
def Delivered(request):
    restaurant,kitchen = initiate_restaurant_kitchen(request)
    delivered = models.Ordered.objects.select_related().filter(Q(status = 'R')|
                                                               Q(order__status = 'W')|
                                                               Q(status = 'P'),kitchen=kitchen)
    return render(request, 'kitchen/delivered.html', {'delivered':delivered,"kitchen": kitchen})

def Print(request, id):
    order = models.Ordered.objects.get(id = id)
    return render(request, 'kitchen/components/print.html', {'order': order,"kitchen": models.Kitchen.objects.all()[0]})
@login_required
@kitchen_only
def ActiveOrders(request):
    kitchen_instance = models.Kitchen.objects.select_related().filter(attendants=request.user)[0]
    context = {
        "kitchen": kitchen_instance
    }
    # why can't we just get Pending orders to be our Active Orders 
    context['object'] = models.Ordered.objects.select_related().filter(kitchen=kitchen_instance, status = 'P')
    return render(request, 'kitchen/kitchen_active_orders.html',context)
    

@login_required
@kitchen_only
def Dashboard(request):
    restaurant,kitchen = initiate_restaurant_kitchen(request)
    context = {
        "active_orders": get_active_orders(kitchen).order_by('-order__ordered_date'),
        "available_foods": kitchen.available_foods.count(),
        "not_available_foods": kitchen.foods_not_available,
        "all_foods": kitchen.foods.all().count(),
        "kitchen": kitchen
    }
    return render(request, 'kitchen/kitchen_dashboard.html', context)

@login_required
@kitchen_only
def CustomerOrders(request):
    context = {
        "object": models.Ordered.objects.all(),
        "kitchen": models.Kitchen.objects.all()[0]
    }
    return render(request, 'kitchen_customer_view.html', context)

@login_required
@kitchen_only
def Add_food(request):
    restaurant,kitchen = initiate_restaurant_kitchen(request)
    if request.POST:
        food = models.Food()
        food.name = request.POST.get('name')
        food.price = request.POST.get('price')
        food.quantity = request.POST.get('quantity')
        food.image = request.FILES.get('image')
        food.category = models.Category.objects.get(name = request.POST.get('category'))
        food.save()
        kitchen.foods.add(food)
        
    context = {
        "categories": models.Category.objects.all(),
        "kitchen": kitchen
    }
    return render(request, 'kitchen/add_food.html', context)

@login_required
@kitchen_only
def Manage_Food(request, page):
    restaurant,kitchen = initiate_restaurant_kitchen(request)
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        food = request.POST.get('food')
        f = kitchen.foods.get(id = food)
        f.quantity = int(quantity)
        f.name = name
        f.price = price
        f.save()
    if page == 'not':
        foods = kitchen.foods.filter(quantity__lte=1).order_by('quantity')
    elif page == 'all':
        foods = kitchen.foods.all().order_by('quantity')
    else:
        foods = kitchen.foods.filter(quantity__gte=1).order_by('quantity')
        
    return render(request, 'kitchen/foods.html', {'foods': foods, 'kitchen':kitchen})

@login_required
@kitchen_only
def SaveFood(request, food_id):
    data = json.loads(request.body)
    food = models.Food.objects.get(id = food_id)
    if request.method == 'DELETE':
        food.delete()
        return JsonResponse({'success':True})
    food.name = data.get('name')
    food.price = data.get('price')
    food.quantity = data.get('quantity')
    food.save()
    return JsonResponse({'success':True})


@login_required
@kitchen_only
def OrderConfirm(request, order_id):
    order = models.Ordered.objects.get(id=order_id)
    order.status = 'D'
    order.save()
    # messages.info(request,'Order Status Changed to Delivered')
    return JsonResponse({'success': True})

@login_required
@kitchen_only
def OrderDecline(request, order_id):
    
    if request.method == 'POST':
        import json 
        order = models.Ordered.objects.get(id=order_id)
        order.status = 'R'
        order.save()
        reason = models.OrderFeed()
        reason.feed = json.loads(request.body).get('reason')
        reason.item = order
        reason.save()
        # messages.info(request,'Order Status Changed to Rejected')
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
