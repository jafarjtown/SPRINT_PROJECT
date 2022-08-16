from django.db import models

from authentication.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=25)
    image = models.ImageField()
    
    def __str__(self) -> str:
        return f'{self.name} category'

class Food(models.Model):
    name = models.CharField(max_length=25)
    price = models.FloatField()
    quantity = models.IntegerField()
    image = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='foods')
    kitchen_offered = models.ForeignKey('Kitchen', on_delete=models.CASCADE, null=True, blank=True, related_name='foods')
    
class Kitchen(models.Model):
    attendants = models.ManyToManyField(User,blank=True)
    
    @property
    def foods_not_available(self):
        return len(self.foods.filter(quantity__lte = 1))
    
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('administrator:kitchen', kwargs={'kitchen_id': self.pk})
    
    @property
    def available_foods(self):
        return self.foods.filter(quantity__gte = 1)
    
    @property
    def waiting_order(self):
        return self.ordered.filter(delivered = False)
    
    @property
    def orders_sum(self):
        obj = {}
        for o in self.ordered.all():
            if obj.get(str(o.order.ordered_date)) == None:
                obj[str(o.order.ordered_date)] = {'items': [], 'date': o.order.ordered_date, 'total': 0}
            obj[str(o.order.ordered_date)]['items'].append(o)
            obj[str(o.order.ordered_date)]['total'] += (int(o.price) * int(o.quantity))
            # ord.add(o.order)
        return obj.values()

class Payment(models.Model):
    pass

class Ordered(models.Model):
    name = models.CharField(max_length=25)
    image = models.CharField(blank=True, max_length=50)
    price = models.FloatField()
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    delivered = models.BooleanField(default=False)
    delivery_point = models.TextField()
    phone_no = models.CharField(max_length=15)
    kitchen = models.ForeignKey(Kitchen, on_delete=models.SET_NULL, null=True, related_name='ordered')
    time = models.TimeField(auto_now_add=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, blank=True, null=True, related_name='items')
    
    @property
    def get_kitchen_await_orders(self):
        orders = self.objects.filter(kitchen=self.kitchen,delivered=False)
        return len(orders)
    
    @property
    def total_price(self):
        return self.price * self.quantity
    
    @property
    def customer(self):
        return self.order.customer
    
    @property
    def date(self):
        return self.order.ordered_date

class Order(models.Model):
    customer = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True)
    # for date only
    ordered_date = models.DateField()
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, blank=True, null=True)
    is_delivered = models.BooleanField(default=True)
    
    @property
    def get_kitchen_await_orders(self):
        orders = self.objects.filter(kitchen=self.kitchen,delivered=False)
        return len(orders)

    @property
    def total(self):
        return sum([item.price for item in self.items.all()])
    
    @property
    def quantity(self):
        return sum([items.quantity for items in self.items.all()])
    

class News(models.Model):
    date = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=500)

    