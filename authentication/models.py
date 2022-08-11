from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

ACCOUNT_TYPE = (
    ('Staff', 'Staff'),
    ('Student', 'Student'),
    ('Other', 'Other'),
)

class User(AbstractUser):
    date_of_birth = models.DateField(null=True)
    phone_no = models.CharField(max_length=15)
    account_type = models.CharField(choices=ACCOUNT_TYPE, default=ACCOUNT_TYPE[1], max_length=10)
    account_id = models.CharField(max_length=50)
    #to know wether account is kitchen or customers
    is_kitchen = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    gender = models.CharField(max_length=10)
    pass


    def orders(self):
        all_orders = list()
        
        for order in self.order_set.all():
            all_orders.extend(order.items.all())
        return all_orders
    
    @property
    def recents_orders(self):
        return self.orders()[:5]