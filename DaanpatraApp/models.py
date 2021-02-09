import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

ROLE_CHOICES = (
    ("Super_Admin", "Super Admin"),
    ("Sub_Admin", "Sub Admin"),
    ("driver", "Driver"),
    ("user", "User"),
)

CATEGORY = (
    ("clothes", "Clothes"),
    ("food", "Raw Food"),
    # ("fund", "Fund"),
    ("utensils", "Utensils"),
    ("equipments", "Equipments"),
    ("books", "Books"),
    ("medicines", "Un-Expired Medicines"),
    ("other", "Other"),
)

class User(AbstractUser):
    profile = models.ImageField(upload_to='Profile Pictures', blank=True, null=True)
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    email = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=150, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length = 30,choices = ROLE_CHOICES, default='user')
    otp = models.CharField(max_length = 30,null=True, blank=True)
    contact = models.CharField(max_length = 30,null=True, blank=True)

    class Meta:
        permissions = ( 
            ("can_add_sub_admin", "Access to add Sub Admin"),
            ("can_update_sub_admin", "Access to update Sub Admin"),
            ("can_remove_sub_admin", "Access to remove Sub Admin"),
            ("can_add_drivers", "Access to add Drivers"), 
            ("can_remove_drivers", "Access to remove Drivers"),
            ("can_update_drivers", "Access to update Drivers"),
            ("can_add_location", "Access to add location"),
            ("can_remove_location", "Access to remove location"),
            ("can_update_location", "Access to update location"), 
            ("can_update_donation_status", "Access to update Donation Status"),
            ("can_get_donation_gallery_images", "Access to get Donation Gallery Images"),
            ("can_add_donation_gallery_images", "Access to Add Donation Gallery Images"),
            ("can_remove_donation_gallery_images", "Access to Delete Donation Gallery Images"), 
        )

    # def __str__(self):
    #     return self.first_name

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User', blank=True, null=True)
    product_category = models.CharField(max_length = 30,choices = CATEGORY)
    product_description = models.CharField(max_length = 250)
    quantity = models.IntegerField(default=10, validators=[MinValueValidator(10)])
    pickup_address = models.CharField(max_length = 150)
    pickup_time = models.TimeField()
    pickup_date = models.DateField()
    assign_to_sub_admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Assigned_to_Sub_Admin', blank=True, null=True)
    assign_to_driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Assigned_to_drivers', blank=True, null=True)
    donation_status = models.BooleanField(default=False,help_text = "Check when delivery gets successful.")

class ProductImages(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='Product_Images', blank=True, null=True)
    images = models.ImageField(upload_to='Donation Product Image', blank=True, null=True)


class DonationGallery(models.Model):
    images = models.ImageField(upload_to='Donation Gallery', blank=True, null=True)


# class FundDonation(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     amount = models.IntegerField()
#     time = models.TimeField(blank=True, null=True)
#     date = models.DateField(blank=True, null=True)

#     def __str__(self):
#         return self.user.name