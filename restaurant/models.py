from django.db import models

# Create your models here.


class CustomerChat(models.Model):
    attendant = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True, related_name='customer_chats')
    customer = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True, related_name='kitchen_chats')
    messages = models.ManyToManyField('administrator.Message', blank=True)
    