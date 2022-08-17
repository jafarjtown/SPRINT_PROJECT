from django.urls import path
from . import views

app_name = 'kitchen'

urlpatterns = [
    path('', views.Dashboard, name='dashboard'),
    path('customers-orders/', views.CustomerOrders, name='customer-orders'),
    path('active-orders/', views.ActiveOrders, name='active-orders'),
    path('orders/', views.Orders, name='orders'),
    path('orders/<str:order_id>/confirm/', views.OrderConfirm, name='confirm-order'),
    path('orders/<str:order_id>/decline/', views.OrderDecline, name='decline-order'),
    path('add-food/', views.Add_food, name='add-food'),
    path('manage-food/', views.Manage_Food, name='manage-food'),
    path('not-available/', views.NotAvailable, name='not-available-food'),
]
