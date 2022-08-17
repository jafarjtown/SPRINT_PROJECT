from django.db import models

from kitchen.models import Ordered

# Create your models here.

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
    
    @property
    def not_available_foods(self):
        kitchen = self.kitchen
        return kitchen.foods.filter(quantity__lt=1)
    
    @property
    def foods_not_available(self):
        kt = self.kitchen
        not_available = kt.foods_not_available
        return not_available
    @property
    def foods(self):
        kt = self.kitchen
        return kt.available_foods
    
    @property
    def orders(self):
        kt = self.kitchen
        return Ordered.objects.all()
    
    @property
    def orders_sum(self):
        obj = {}
        for o in Ordered.objects.all():
            if obj.get(str(o.order.ordered_date)) == None:
                obj[str(o.order.ordered_date)] = {'items': [], 'date': o.order.ordered_date, 'total': 0}
            obj[str(o.order.ordered_date)]['items'].append(o)
            obj[str(o.order.ordered_date)]['total'] += (int(o.price) * int(o.quantity))
        print(obj)
        return obj.values()