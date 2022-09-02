from datetime import date
from django.shortcuts import redirect, render
from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from administrator.forms import BlogForm
from administrator.models import Activity, Blog, Message, RestaurantService
from authentication.models import User
from decorators import administrator_only, is_logged_in
from django.contrib.messages import add_message, constants
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password,  make_password

from kitchen.models import Food, Kitchen, Ordered, Category
# Create your views here.

def generate_username_with_prefix(admin):
    # name
    
    name = ''.join(list(admin.name))
    if len(name) > 5:
        name = name[:6].lower() + str(admin.kitchen.attendants.count() + 1)
    admin.activities.add(Activity.objects.create(message=f'new Username is generated -> {name}.'))
    return name

def initiate_admin_kitchen(request):
    admin = RestaurantService.objects.get(admin=request.user)
    kitchen_instance = admin.kitchen
    return admin, kitchen_instance

def get_this_week_sells(total):
    FROM = 9
    today = date.today()
    last_weeks = total.filter(
        order__ordered_date__year = today.year,
        order__ordered_date__month = today.month,
        order__ordered_date__day__gte = (today.day - FROM))
    return last_weeks

def get_total_sells(admin):
    return Ordered.objects.filter(kitchen = admin.kitchen, order__payment__is_payed = True, status='D')
def get_customers(sells):
    customers = set(sell.order.customer for sell in sells)
    return customers

@login_required
@administrator_only
def Dashboard(request):
    admin,kitchen_instance = initiate_admin_kitchen(request)
    total_sell = get_total_sells(admin)
    this_week_sell = get_this_week_sells(total_sell)
    today_sell = this_week_sell.filter(order__ordered_date__day = (date.today().day))
    customers = get_customers(total_sell)
    last_few_recents = total_sell.order_by('order__ordered_date')[:10]
    activities = admin.activities.all().order_by('-datetimestamp')
    context = {
        'restaurant': kitchen_instance, 
        'customers':customers, 
        'today_sell':today_sell, 
        'this_week_sell':this_week_sell, 
        'total_sell':total_sell,
        'activities':activities,
        'last_few_recents':last_few_recents
        }
    return render(request, 'administrator/dashboard.html',context)

@login_required
@administrator_only
def FoodifyChat(request):
    admin,_ = initiate_admin_kitchen(request)
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
        admin.foodify_chat.add(message)
        admin.save()
        return redirect('administrator:foodify-chat')
    messages = admin.foodify_chat.all()[:15]
    return render(request, 'administrator/stemchat-public.html', {'msgs':messages})

@login_required
@administrator_only
def StaffChat(request):
    admin,_ = initiate_admin_kitchen(request)
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
        admin.staff_chat.add(message)
        admin.save()
        return redirect('administrator:staff-chat')
    messages = admin.staff_chat.all()[:15]
    return render(request, 'administrator/stemchat.html', {'msgs':messages})


@login_required
@administrator_only
def UpdateProfile(request):
    user = request.user
    admin,_ = initiate_admin_kitchen(request)
    if request.method == 'POST':
        if request.FILES.get('profile-pic'):
            user.profile_picture = request.FILES.get('profile-pic')
        user.first_name, user.last_name = request.POST.get('full_name').split(' ' or ',')
        user.phone_no = request.POST.get('phone_no')
        if request.POST.get('gender'):
            user.gender = request.POST.get('gender')
        
        user.save()
        return redirect('administrator:profile')
    return render(request, 'administrator/profile.html',{'restaurant':admin})

@login_required
@administrator_only
def Orders(request):
    admin,kitchen_instance = initiate_admin_kitchen(request)
    total_sell = get_total_sells(admin)
    return render(request, 'administrator/orders.html', {'orders': total_sell})




# i do not touch

@login_required
@administrator_only
def Profile(request):
    admin,_ = initiate_admin_kitchen(request)
    return render(request, 'administrator/profile-view.html', {'restaurant':admin})

@login_required
@administrator_only
def Foods(request):
    admin = RestaurantService.objects.get(admin=request.user)
    kitchen_instance = Kitchen.objects.select_related().filter(restaurant_kitchen=admin)[0]

    foods = kitchen_instance.available_foods
    print(foods, kitchen_instance)
    return render(request, 'administrator/foods.html', {'foods': foods})


@login_required
@administrator_only
def KitchenView(request):
    admin,kitchen = initiate_admin_kitchen(request)
    attendants = kitchen.attendants.all()
    return render(request, 'administrator/kitchen.html', {'kitchen': kitchen, 'attendants':attendants})

@login_required
@administrator_only
def SuspendAttendant(request, attendant_id):
    try:
        admin,kitchen = initiate_admin_kitchen(request)
        attendant = kitchen.attendants.get(id = attendant_id)
        if attendant.is_active:
            attendant.is_active = False
            act = Activity.objects.create(message=f'you Suspend {attendant.get_full_name()}.') 
        else:
            attendant.is_active = True
            act = Activity.objects.create(message=f'you Unsuspend {attendant.get_full_name()}.')
        admin.activities.add(act)
        attendant.save()
        return JsonResponse({'success': True})
        
    except:
        return JsonResponse({'success': False})

@login_required
@administrator_only
def DeleteAttendant(request, attendant_id):
    try:
        admin,kitchen = initiate_admin_kitchen(request)
        attendant = kitchen.attendants.get(id = attendant_id)
        attendant.delete()
        act = Activity.objects.create(message=f'you remove {attendant.get_full_name} from your kitchen.')
        admin.activities.add(act)
        return JsonResponse({'success': True})
            
    except:
        return JsonResponse({'success': False})

@login_required
@administrator_only
def AssignKitchenAttendant(request):

    if request.method == 'POST':
        admin,kitchen = initiate_admin_kitchen(request)
        try:
            u = generate_username_with_prefix(admin)
            print(u)
            dob = request.POST.get('date_of_birth')
            f, l = request.POST.get('full_name').split(' ')

            e = request.POST.get('email')
            g = request.POST.get('gender')
            ph = request.POST.get('phone_no')
            p1 = request.POST.get('password')
            attendant = User.objects.create_user(
                username=u, 
                first_name=f,
                last_name=l,
                email=e,
                gender=g,
                date_of_birth=dob,
                phone_no=ph,
                password=p1,
                is_kitchen = True)
            kitchen.attendants.add(attendant)
            kitchen.save()
            attendant.save()
            admin.activities.add(Activity.objects.create(message=f'You add a new Attendant -> {u} to your kitchen'))
            return redirect('administrator:kitchen')
        except Exception as e:
            print(e)
            return redirect('administrator:dashboard')
    return render(request, 'administrator/new-kitchen-attendant.html')

@login_required
@administrator_only
def DeclinedOrder(request, order_id):
    ordered = Ordered.objects.get(id=order_id)
    try:
        order = ordered.kitchen.foods.get(name=ordered.name)
        order.quantity = F('quantity') + ordered.quantity
        order.save()
        ordered.delete()
    except ObjectDoesNotExist:
        ordered.delete()
    return redirect('administrator:orders')

@login_required
@administrator_only
def Categories(request):
    categories = Category.objects.all()
    return render(request, 'administrator/categories.html', {'categories': categories})

@login_required
@administrator_only
def NewCategory(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        Category.objects.create(name=name, image=image)
        return redirect('administrator:category')
    return render(request, 'administrator/category.html')

@login_required
def ChangePassword(request):
    if request.method == 'POST':
        user = request.user
        current_password = request.POST.get('current password')
        new_password = request.POST.get('new password')
        confirm_password = request.POST.get('confirm password')
        if check_password(current_password, user.password):
            if new_password == confirm_password:
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
                add_message(request, constants.ERROR,
                            'This is Account didnt have access to administrator dashboard')
                return redirect('administrator:login')
            login(request, user)
            add_message(request, constants.SUCCESS, 'login success')
            if user.is_kitchen:
                return redirect('kitchen:dashboard')
            elif user.is_admin:
                return redirect('administrator:dashboard')
            return redirect('restaurant:dashboard')
        add_message(request, constants.ERROR, 'Invalid credentials')
    return render(request, 'administrator/login.html')
