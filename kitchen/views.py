
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from administrator.views import Category
from decorators import is_logged_in, kitchen_only
from administrator.models import Message
# from administrator.views import Category
from . import models

# Create your views here.

#TODO: Active Orders page (confirm/decline)
#TODO: Dashboard
#TODO: Login
#TODO: News
#TODO: Customer Orders

@login_required
@kitchen_only
def StemChat(request):
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
        return redirect('kitchen:chat')
    messages = Message.objects.all()[:15]
    return render(request, 'kitchen/stemchat.html', {'msgs':messages})

@login_required
@kitchen_only
def Orders(request):
    # ord = list()
    kitchen = models.Kitchen.objects.all()[0]
    
    # .....
    # lets get the ordered item all at once without
    # looping through Orders
    orders = models.Ordered.objects.all()
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
    return render(request, 'kitchen/orders.html', {'orders': orders, 'kitchen':kitchen})

@login_required
@kitchen_only
def Delivered(request):
    orders = models.Ordered.objects.filter(status = 'D')
    return render(request, 'kitchen/delivered.html', {'orders':orders,"kitchen": models.Kitchen.objects.all()[0]})

def Print(request, id):
    order = models.Ordered.objects.get(id = id)
    return render(request, 'kitchen/components/print.html', {'order': order,"kitchen": models.Kitchen.objects.all()[0]})
@login_required
@kitchen_only
def ActiveOrders(request):
    context = {
        "object": models.Order.objects.filter(is_delivered=False),
        "kitchen": models.Kitchen.objects.all()[0]
    }
    # why can't we just get Pending orders to be our Active Orders 
    context['object'] = models.Ordered.objects.filter(status = 'P')
    return render(request, 'kitchen/kitchen_active_orders.html',context)
    # return render(request, 'kitchen/kitchen_active_orders.html',context)

@login_required
@kitchen_only
def Dashboard(request):
    context = {
        "orders": models.Ordered.objects.all(),
        "user": request.user,
        "kitchen": models.Kitchen.objects.all()[0]
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

@login_required
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
    
    if request.method == 'POST':
        order = models.Ordered.objects.get(id=order_id)
        order.status = 'R'
        order.save()
        reason = models.OrderFeed()
        reason.feed = request.POST.get('reason')
        reason.item = order
        reason.save()
        messages.info(request,'Order Status Changed to Rejected')
        return redirect('kitchen:orders')
    return render(request, 'kitchen/decline-order.html')

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