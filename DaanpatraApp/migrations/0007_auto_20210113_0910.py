# Generated by Django 3.1.5 on 2021-01-13 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DaanpatraApp', '0006_donation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='assign_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Assigned_to', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='donation',
            name='pickup_address',
            field=models.CharField(max_length=150),
        ),
    ]
