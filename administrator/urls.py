
from django.urls import path
from . import views

app_name = 'administrator'
urlpatterns = [
    path('', views.Dashboard, name='dashboard'),
    path('orders/', views.Orders, name='orders'),
    path('profile/', views.Profile, name='profile'),
    path('foods/', views.Foods, name='foods'),
    path('kitchens/', views.Kitchens, name='kitchens'),
    path('kitchen/<int:kitchen_id>/', views.KitchenView, name='kitchen'),
    path('kitchen/<int:kitchen_id>/orders/', views.KitchenOrders, name='kitchen-orders'),
    path('kitchen/<int:kitchen_id>/orders-summary/', views.KitchenOrdersSummary, name='kitchen-orders-summary'),
    path('assign-attendant-to-kitchen/<int:kitchen_id>/', views.AssignKitchenAttendant, name='assign-attendant'),
    path('new-restaurant/', views.NewRestaurant, name='new-restaurnat'),
    path('new-kitchen/', views.NewKitchen, name='new-kitchen'),
    path('posts/', views.Blogs, name='posts'),
    path('config-post/', views.NewBlog, name='config-post'),
    path('config-post/<int:blog_id>/', views.UpdateBlog, name='update-post'),
    path('customers/', views.StudentCustomers, name='student-customers'),
    path('orders-summary/', views.OrderSummary, name='orders-summary'),
    path('not-available/', views.NotAvailable, name='not-available'),
]
