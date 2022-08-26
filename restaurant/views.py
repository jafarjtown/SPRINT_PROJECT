# from re import M
import imp
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, constants
from django.db.models import F
# from SPRINT_PROJECT.kitchen.models import Food
from administrator.models import Blog, RestaurantService
from administrator.views import Foods
from decorators import customer_only
from kitchen.models import Category as Cat, Food, Kitchen, Order, OrderFeed, Ordered
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
def OrderFood(request, id):
    if request.method == 'POST':
        import datetime
        food = Food.objects.get(id=id)
        today = datetime.date.today()
        order_list = Order.objects.get_or_create(
            ordered_date=today, customer=request.user)
        ordered = Ordered.objects.create(name=food.name, image=food.image.url, price=food.price, quantity=request.POST.get(
            'quantity'), category=food.category, delivery_point=request.POST.get('delivery_point'), phone_no=request.POST.get('phone_no'))
        order_list[0].items.add(ordered)
        order_list[0].save()
        food.quantity = F('quantity') - int(request.POST.get('quantity'))
        food.save()
        return redirect('restaurant:categories')


@login_required
@customer_only
def Dashboard(request):
    user = request.user
    posts = Blog.objects.all()
    recents = user.recents_orders
    return render(request, 'restaurant/dashboard.html', {'posts': posts, 'recents': recents})


@login_required
@customer_only
def OrderStatus(request):
    return render(request, 'restaurant/order-status.html')


@login_required
@customer_only
def OrderHistory(request):
    context = {}
    all_orders = request.user.order_set.all()
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
