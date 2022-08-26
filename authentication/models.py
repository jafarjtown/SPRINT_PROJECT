from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.

ACCOUNT_TYPE = (
    ('Staff', 'Staff'),
    ('Student', 'Student'),
    ('Other', 'Other'),
)

GENDER = (
    ('M','Male'),
    ('F','Female'),
    ('O','Others',)
)

class User(AbstractUser):
    date_of_birth = models.DateField(null=True)
    phone_no = models.CharField(max_length=15)
    account_type = models.CharField(choices=ACCOUNT_TYPE, default=ACCOUNT_TYPE[1], max_length=10)
    account_id = models.CharField(max_length=50)
    #to know wether account is kitchen or customers
    is_kitchen = models.BooleanField(default=False)
    gender = models.CharField(choices=GENDER, max_length=1)
    profile_picture = models.ImageField(upload_to='avatar-pic')
    pass


    @property
    def is_admin(self):
        return self.is_superuser

    def orders(self):
        all_orders = list()
        
        for order in self.cart_order.filter(status = 'C'):
            all_orders.extend(order.items.all())
        return all_orders
    
    @property
    def carts(self):
        return self.cart_order.filter(payment_type = 'N').last()
    
    @property
    def recents_orders(self):
        all_orders = list()
        
        for order in self.cart_order.all():
            all_orders.extend(order.items.filter(status = 'P'))
        return all_orders
    
    @property
    def waiting_orders(self):
        all_orders = list()
        
        for order in self.order_set.all():
            all_orders.extend(order.items.filter(models.Q(status = 'P')|models.Q(status = 'R')))
        return all_orders


        