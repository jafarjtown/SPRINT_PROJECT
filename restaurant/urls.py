
from django.urls import path

from .views import About, AddToCart, AllFoods, CancelOrder, Cart, Category, CategoryList, Dashboard, Home, Order_feed, OrderFood, OrderHistory, OrderPending, OrderStatus, PostHome, Profile, UpdateProfile

app_name = 'restaurant'

urlpatterns = [
    path('', Home, name='welcome'),
    path('all_foods', AllFoods, name='all-foods'),
    path('blog/<int:post_id>/', PostHome, name='blog'),
    path('categories/', Category, name='categories'),
    path('categories/<str:category>/', CategoryList, name='category-list'),
    path('about/', About, name='about'),
    path('dashboard/', Dashboard, name='dashboard'),
    path('dashboard/profile/', Profile, name='profile'),
    path('dashboard/cart/', Cart, name='cart'),
    path('dashboard/order-feed/<int:feed_id>/', Order_feed, name='feed'),
    path('dashboard/profile/update/', UpdateProfile, name='update_profile'),
    path('dashboard/order-status/', OrderStatus, name='order-status'),
    path('dashboard/order-history/', OrderHistory, name='order-history'),
    path('dashboard/order-pending/', OrderPending, name='order-pending'),
    path('dashboard/order-food/<int:id>/', OrderFood, name='order-food'),
    path('dashboard/order-food/add-to-cart/<int:id>/', AddToCart, name='add-to-cart'),
    path('dashboard/order-cancel/<int:order_id>/', CancelOrder, name='cancel-order'),
]
