# Generated by Django 4.2.5 on 2023-09-29 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_parkingslot_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingslot',
            name='unique_id',
            field=models.CharField(auto_created=True, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
