from multiprocessing import context
from django import forms
from django.shortcuts import render
#don't know 🤔 why you add it
#from requests import request

from . import models

# Create your views here.

#TODO: Active Orders page (confirm/decline)
#TODO: Dashboard
#TODO: Login
#TODO: News
#TODO: Customer Orders

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
    return render(request, 'kitchen_dashboard.html', context)
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
        food.name = request.POST.get('price')
        food.name = request.POST.get('quantity')
        food.name = request.POST.get('image')
        food.name = request.POST.get('category')
    context = {
        "categories": models.Category.objects.all()
    }
    return render(request, 'add_food.html', context)
