# Generated by Django 4.2.5 on 2023-09-29 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_parkingslot_unique_id_parkingslot_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkingslot',
            name='unique_id',
            field=models.IntegerField(auto_created=True, default=1, unique=True),
            preserve_default=False,
        ),
    ]