
from django.urls import path
from . import views
from authentication.views import Login

app_name = 'administrator'
urlpatterns = [
    path('', views.Dashboard, name='dashboard'),
    path('login/', views.AdminLogin , name='login'),
    path('change-password/', views.ChangePassword , name='change-password'),
    path('orders/', views.Orders, name='orders'),
    path('orders/declined/<int:order_id>/', views.DeclinedOrder, name='declined-orders'),
    path('profile/', views.Profile, name='profile'),
    path('profile/update/', views.UpdateProfile, name='update-profile'),
    path('profile/<str:username>/', views.CustomerProfile, name='customer-profile'),
    path('foods/', views.Foods, name='foods'),
    path('foods/add', views.AddFood, name='add-food'),
    path('kitchen/', views.KitchenView, name='kitchen'),
    path('kitchen/suspend/<int:attendant_id>/', views.SuspendAttendant, name='suspend-attendant'),
    path('kitchen/delete/<int:attendant_id>/', views.DeleteAttendant, name='delete-attendant'),
    path('kitchen/orders/', views.KitchenOrders, name='kitchen-orders'),
    path('kitchen/orders-summary/', views.KitchenOrdersSummary, name='kitchen-orders-summary'),
    path('add-attendant-to-kitchen/', views.AssignKitchenAttendant, name='add-attendant'),
    path('new-restaurant/', views.NewRestaurant, name='new-restaurnat'),
    path('category/', views.Categories, name='category'),
    path('category/new/', views.NewCategory, name='new-cat'),
    path('posts/', views.Blogs, name='posts'),
    path('chat/foodify/', views.FoodifyChat, name='foodify-chat'),
    path('chat/staff/', views.StaffChat, name='staff-chat'),
    path('config-post/', views.NewBlog, name='config-post'),
    path('config-post/<int:blog_id>/', views.UpdateBlog, name='update-post'),
    path('customers/', views.StudentCustomers, name='student-customers'),
    path('orders-summary/', views.OrderSummary, name='orders-summary'),
    path('orders-summary/<date>/', views.PrintOrderSummary, name='print-orders-summary'),
    path('not-available/', views.NotAvailable, name='not-available'),
]
