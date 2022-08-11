# Generated by Django 4.0.2 on 2022-08-11 01:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administrator', '0001_initial'),
        ('kitchen', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantservice',
            name='admin',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='restaurant', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='restaurantservice',
            name='kitchens',
            field=models.ManyToManyField(related_name='restaurant', to='kitchen.Kitchen'),
        ),
        migrations.AddField(
            model_name='blogcomment',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.blog'),
        ),
        migrations.AddField(
            model_name='blog',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
