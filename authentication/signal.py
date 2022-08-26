from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def signal(sender, instance, created):
    if created:
        if instance.is_kitchen:
            pass