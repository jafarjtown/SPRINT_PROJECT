
from django.urls import path
from . import views

app_name = 'administrator'
urlpatterns = [
    path('', views.Dashboard, name='dashboard'),
    path('login/', views.AdminLogin , name='login'),
    path('change-password/', views.ChangePassword , name='change-password'),
    path('orders/', views.Orders, name='orders'),
    path('orders/declined/<int:order_id>/', views.DeclinedOrder, name='declined-orders'),
    path('profile/', views.Profile, name='profile'),
    path('profile/update/', views.UpdateProfile, name='update-profile'),
    path('foods/', views.Foods, name='foods'),
    path('kitchen/', views.KitchenView, name='kitchen'),
    path('kitchen/suspend/<int:attendant_id>/', views.SuspendAttendant, name='suspend-attendant'),
    path('kitchen/delete/<int:attendant_id>/', views.DeleteAttendant, name='delete-attendant'),
    path('add-attendant-to-kitchen/', views.AssignKitchenAttendant, name='add-attendant'),
    path('category/', views.Categories, name='category'),
    path('category/new/', views.NewCategory, name='new-cat'),
    path('chat/foodify/', views.FoodifyChat, name='foodify-chat'),
    path('chat/staff/', views.StaffChat, name='staff-chat'),
]