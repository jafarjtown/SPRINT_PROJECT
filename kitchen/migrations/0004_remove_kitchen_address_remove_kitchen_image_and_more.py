# Generated by Django 4.0.2 on 2022-08-15 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0003_alter_kitchen_attendant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kitchen',
            name='address',
        ),
        migrations.RemoveField(
            model_name='kitchen',
            name='image',
        ),
        migrations.RemoveField(
            model_name='kitchen',
            name='name',
        ),
        migrations.RemoveField(
            model_name='kitchen',
            name='phone_number',
        ),
    ]
