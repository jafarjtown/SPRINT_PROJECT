# from re import M

import json
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, constants
from django.db.models import F
# from SPRINT_PROJECT.kitchen.models import Food
from administrator.models import Blog, RestaurantService
from administrator.views import Foods
from decorators import customer_only
from kitchen.models import Category as Cat, Food, Kitchen, Order, OrderFeed, Ordered, Payment
# Create your views here.


def Home(request):
    return render(request, 'restaurant/index.html')


def Category(request):
    categories = Cat.objects.all()
    context = {'categories': categories}
    if request.GET.get('food'):
        food = request.GET.get('food')
        rest = request.GET.get('restaurant')
        cat = request.GET.get('category')
        search = None
        result = Food.objects.filter(name__icontains = food)
        if rest != 'all':
            result = result
        if cat != 'all':
            result = result.filter(category__name = cat)
        context['foods'] = result
        context['search'] = True
        context['result_count'] = len(result)
    return render(request, 'restaurant/categories.html', context)

def Cart(request):
    customer_order = Order.objects.filter(customer=request.user).last()
    context = {'customer_order': customer_order}
    if request.method == 'POST':
        customer_order.delivery_point = request.POST.get('delivery_point') 
        customer_order.phone_no = request.POST.get('phone_number')
        customer_order.payment_type = request.POST.get('payment_type')
        customer_order.save()
    return render(request, 'restaurant/cart.html', context)


def PaymentSuccess(request, order_id):
    if request.method == 'POST':
        import json
        if request.body:
            data = json.loads(request.body)
        else:
            data = request.POST
        ref = data['ref']  
        delivery_point = data['delivery_point']  
        phone_no = data['phone_no']  
        customer_order = Order.objects.get(id = order_id)
        customer_order.status = 'C'
        customer_order.payment_type = 'O'
        customer_order.delivery_point = delivery_point
        customer_order.phone_no = phone_no
        payment = Payment()
        payment.ref_id = ref
        payment.user = request.user
        payment.amount = customer_order.total
        payment.is_payed = True
        payment.save()
        customer_order.payment = payment
        customer_order.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def AllFoods(request):
    foods = Food.objects.filter(quantity__gte=1)
    context = {"category": 'All Foods', 'foods': foods}
    return render(request, 'restaurant/cat-list.html', context)


def CategoryList(request, category):
    try:
        foods = Cat.objects.get(name=category).foods.filter(quantity__gte=1)
        context = {"category": category, 'foods': foods}
        return render(request, 'restaurant/cat-list.html', context)
    except:
        return redirect('restaurant:categories')


def PostHome(request, post_id):
    post = Blog.objects.get(id=post_id)
    if request.method == 'POST':
        username = request.POST.get('username') or 'Anonymous'
        body = request.POST.get('body')

    return render(request, 'restaurant/posts.html', {'post': post})


def About(request):
    return render(request, 'restaurant/about.html')

@login_required
@customer_only
def AddToCart(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        food = Food.objects.get(id=id)
        order_list,_ = Order.objects.get_or_create(customer=request.user, payment_type='N')
        ordered = Ordered.objects.create(name=food.name, image=food.image.url, price=food.price, quantity=data.get(
            'quantity'), category=food.category, kitchen = food.kitchen_offered)
        order_list.items.add(ordered)
        food.quantity = F('quantity') - int(data.get('quantity'))
        order_list.save()
        food.save()
        return JsonResponse({'success': True})

@login_required
@customer_only
def OrderFood(request, id):

    if request.method == 'POST':
        order_list,_ = Order.objects.get_or_create(customer=request.user, payment_type='N')
        order_list.delivery_point = request.POST.get('delivery_point'), 
        order_list.phone_no = request.POST.get('phone_no')
        order_list.save()
        return redirect('restaurant:categories')


@login_required
@customer_only
def Dashboard(request):
    user = request.user
    posts = Blog.objects.all()
    foods = Food.objects.all()
    recents = user.recents_orders
    return render(request, 'restaurant/dashboard.html', {'posts': posts, 'recents': recents, 'foods':foods})


@login_required
@customer_only
def OrderStatus(request):
    return render(request, 'restaurant/order-status.html')


@login_required
@customer_only
def OrderHistory(request):
    context = {}
    all_orders = request.user.orders()
    context['orders'] = all_orders
    return render(request, 'restaurant/order-history.html', context)


@login_required
@customer_only
def OrderPending(request):
    orders = request.user.waiting_orders
    return render(request, 'restaurant/order-pending.html', {'orders':orders})

@login_required
@customer_only
def Order_feed(request, feed_id):
    feed = OrderFeed.objects.get(id = feed_id)
    return render(request, 'restaurant/feed.html', {'feed':feed})


@login_required
def Profile(request):
    return render(request, 'restaurant/profile.html')

@login_required
def CancelOrder(request, order_id):
    ordered = Ordered.objects.get(id=order_id)
    order = Food.objects.get(name=ordered.name)
    order.quantity = F('quantity') + ordered.quantity
    order.save()
    ordered.delete()
    return redirect('restaurant:dashboard')


@login_required
@customer_only
def UpdateProfile(request):
    if request.method == 'POST':
        user = request.user
        data = request.POST
        if data.get('email'):
            user.email = data.get('email')
        if data.get('date of birth'):
            user.date_of_birth = data.get('date of birth')
        if data.get('phone no'):
            user.phone_no = data.get('phone no')
        if data.get('gender'):
            user.gender = data.get('gender')
        if data.get('full name'):
            first_name, last_name = data.get('full name').split(' ')
            user.first_name = first_name
            user.last_name = last_name
        user.save()
        add_message(request, constants.SUCCESS, 'Profile Updated')
    return render(request, 'restaurant/update_profile.html')
