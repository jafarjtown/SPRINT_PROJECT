from django.db import models

from kitchen.models import Ordered
import datetime
# Create your models here.

class Activity(models.Model):
    datetimestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=300)

class Message(models.Model):
    sender = models.CharField(max_length=25)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    attached_file = models.ImageField(upload_to='message/files/')

class Blog(models.Model):
    author = models.ForeignKey('authentication.User', models.SET_NULL, null=True,  related_name='posts')
    body = models.TextField()
    
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('restaurant:blog', kwargs={'post_id': self.pk})

class RestaurantService(models.Model):
    admin = models.OneToOneField('authentication.User', on_delete=models.SET_NULL, null=True,  related_name='restaurant_admin')
    kitchen = models.OneToOneField('kitchen.Kitchen',on_delete=models.SET_NULL, null=True,  related_name='restaurant_kitchen')
    address = models.TextField()
    name = models.CharField(max_length=25)
    phone_no = models.CharField(max_length=15)
    activities = models.ManyToManyField(Activity, blank=True)
    foodify_chat = models.ManyToManyField(Message, blank=True, related_name='restaurant')
    staff_chat = models.ManyToManyField(Message, blank=True)
    
    @property
    def not_available_foods(self):
        kitchen = self.kitchen.not_available_foods
        return kitchen
    
    @property
    def foods_not_available(self):
        kt = self.kitchen.foods_not_available
        not_available = kt.foods_not_available
        return kt
    @property
    def foods(self):
        kt = self.kitchen
        return kt.available_foods
    
    @property
    def orders(self):
        kt = self.kitchen.orders
        if kt==None:
            return kt
        else: 
            return []
    
    @property
    def orders_sum(self):
        obj = {}
        for o in Ordered.objects.filter(kitchen=self.kitchen):
            if obj.get(str(o.order.ordered_date)) == None:
                obj[str(o.order.ordered_date)] = {'items': [], 'date': o.order.ordered_date, 'total': 0}
            obj[str(o.order.ordered_date)]['items'].append(o)
            obj[str(o.order.ordered_date)]['total'] += (int(o.price) * int(o.quantity))
        print(obj)
        return obj.values()
    
    @property
    def orders_sum_print(self):
        obj = {}
        for o in Ordered.objects.all():
            if obj.get(str(o.order.ordered_date)) == None:
                obj[str(o.order.ordered_date)] = {'items': [], 'date': o.order.ordered_date, 'total': 0}
            obj[str(o.order.ordered_date)]['items'].append(o)
            obj[str(o.order.ordered_date)]['total'] += (int(o.price) * int(o.quantity))
    
        return obj