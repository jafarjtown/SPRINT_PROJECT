from django.db import models

# Create your models here.

class Blog(models.Model):
    author = models.ForeignKey('authentication.User', models.SET_NULL, null=True,  related_name='posts')
    title = models.CharField(max_length=50)
    body = models.TextField()
    
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('restaurant:blog', kwargs={'post_id': self.pk})

class BlogComment(models.Model):
    username = models.CharField(max_length=25)
    body = models.TextField()
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)

class RestaurantService(models.Model):
    admin = models.OneToOneField('authentication.User', models.SET_NULL, null=True,  related_name='restaurant')
    kitchens = models.ManyToManyField('kitchen.Kitchen', related_name='restaurant', )
    address = models.TextField()
    name = models.CharField(max_length=25)
    phone_no = models.CharField(max_length=15)
    
    @property
    def not_available_foods(self):
        foods = list()
        for kitchen in self.kitchens.all():
            foods.extend(kitchen.foods.filter(quantity__lt=1))
        return foods
    
    @property
    def foods_not_available(self):
        not_available = 0
        for kt in self.kitchens.all():
            not_available += kt.foods_not_available
        return not_available
    @property
    def foods(self):
        all_foods = list()
        for kt in self.kitchens.all():
            all_foods.extend(kt.available_foods)
        return all_foods
    
    @property
    def customers(self):
        pass
    
    @property
    def orders(self):
        ord = []
        for kt in self.kitchens.all():
            # print(kt.ordered.all())
            ord.extend(kt.ordered.all())
        # print(ord)
        return ord
    
    @property
    def orders_sum(self):
        ord = set()
        obj = {}
        for kt in self.kitchens.all():
            for o in kt.ordered.all():
                if obj.get(str(o.order.ordered_date)) == None:
                    obj[str(o.order.ordered_date)] = {'items': [], 'date': o.order.ordered_date, 'total': 0}
                obj[str(o.order.ordered_date)]['items'].append(o)
                obj[str(o.order.ordered_date)]['total'] += (int(o.price) * int(o.quantity))
                # ord.add(o.order)
        print(obj)
        return obj.values()