# Generated by Django 4.2.5 on 2023-09-27 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_parking_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parking',
            name='created_by',
        ),
    ]
