from django.urls import path
from . import views

app_name = 'kitchen'

urlpatterns = [
    path('', views.Dashboard, name='dashboard'),
    path('customers-orders/', views.CustomerOrders, name='customer-orders'),
    path('active-orders/', views.ActiveOrders, name='active-orders'),
    path('orders/', views.Orders, name='orders'),
    path('delivered/', views.Delivered, name='delivered'),
    # ..........
    # confirm/decline replace this
    # path('delivered/<int:id>/', views.DeliveredNow, name='delivered-now'),
    # ..........
    # path('news/', views.News, name='news'),
    path('print/<int:id>/', views.Print, name='print'),
    path('orders/<str:order_id>/confirm/', views.OrderConfirm, name='confirm-order'),
    path('orders/<str:order_id>/decline/', views.OrderDecline, name='decline-order'),
    path('add-food/', views.Add_food, name='add-food'),
    path('manage-food/', views.Manage_Food, name='manage-food'),
    path('not-available/', views.NotAvailable, name='not-available-food'),
]
