# Generated by Django 3.1.5 on 2021-01-16 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DaanpatraApp', '0022_user_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('can_add_sub_admin', 'Access to add Sub Admin'), ('can_update_sub_admin', 'Access to update Sub Admin'), ('can_remove_sub_admin', 'Access to remove Sub Admin'), ('can_add_drivers', 'Access to add Drivers'), ('can_remove_drivers', 'Access to remove Drivers'), ('can_update_drivers', 'Access to update Drivers'), ('can_add_location', 'Access to add location'), ('can_remove_location', 'Access to remove location'), ('can_update_location', 'Access to update location'))},
        ),
    ]
