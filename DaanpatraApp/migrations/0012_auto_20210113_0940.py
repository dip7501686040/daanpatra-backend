# Generated by Django 3.1.5 on 2021-01-13 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DaanpatraApp', '0011_auto_20210113_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='product_images',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test', to='DaanpatraApp.test'),
        ),
    ]
