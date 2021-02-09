# Generated by Django 3.1.5 on 2021-01-13 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DaanpatraApp', '0005_delete_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_category', models.CharField(choices=[('clothes', 'Clothes'), ('food', 'Food'), ('fund', 'Fund'), ('utensils', 'Utensils'), ('equipments', 'Equipments'), ('books', 'Books'), ('other', 'Other')], max_length=30)),
                ('product_description', models.CharField(max_length=250)),
                ('quantity', models.IntegerField(default=10)),
                ('pickup_address', models.CharField(choices=[('clothes', 'Clothes'), ('food', 'Food'), ('fund', 'Fund'), ('utensils', 'Utensils'), ('equipments', 'Equipments'), ('books', 'Books'), ('other', 'Other')], max_length=150)),
                ('pickup_time', models.TimeField()),
                ('pickup_date', models.DateField()),
                ('product_images', models.ImageField(upload_to='Images')),
                ('assign_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Assigned_to', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
