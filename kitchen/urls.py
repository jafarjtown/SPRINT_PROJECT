from django.urls import path
from . import views

app_name = 'kitchen'

urlpatterns = [
    path('', views.Dashboard, name='dashboard'),
    path('customers-orders/', views.CustomerOrders, name='customer-orders'),
    path('active-orders/', views.ActiveOrders, name='active-orders'),
    # path('orders/', views.Orders, name='orders'),
    path('orders/', views.Delivered, name='delivered'),
    path('chat/', views.StemChat, name='staff-chat'),
    path('foodify/', views.FoodifyChat, name='foodify-chat'),
    path('print/<int:id>/', views.Print, name='print'),
    path('orders/<str:order_id>/confirm/', views.OrderConfirm, name='confirm-order'),
    path('orders/<str:order_id>/decline/', views.OrderDecline, name='decline-order'),
    path('add-food/', views.Add_food, name='add-food'),
    path('manage-food/<str:page>/state/', views.Manage_Food, name='manage-food'),
    path('manage-food/<int:food_id>/', views.SaveFood, name='save-food'),

]
