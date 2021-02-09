from django.contrib.auth.models import Permission
from rest_framework import serializers
from . models import *
from oauth2_provider.models import AccessToken
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.response import Response
from django.conf import settings
#===========================================================================
class FilteredUserSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        if self.context['request'].user.has_perm('DaanpatraApp.view_user'):
            data = User.objects.all()
            return super(FilteredUserSerializer, self).to_representation(data)
        else:
            raise PermissionDenied()

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        list_serializer_class = FilteredUserSerializer     
        model = User
        fields = "__all__"

    def create(self,validated_data):
        user =  self.context['request'].user
        role = validated_data.get('role')
        if role == 'Sub_Admin':
            if user.has_perm('DaanpatraApp.can_add_sub_admin'):
                user = User.objects.create(
                    email = validated_data.get('email'),
                    username = validated_data.get('username'),
                    password = validated_data.get('password'),
                    first_name = validated_data.get('first_name'),
                    last_name = validated_data.get('last_name'),
                    role=role
                )
                user.set_password(validated_data.get('password'))
                user.save()
                return user
            else:
                raise PermissionDenied()
        else:
            user = User.objects.create(
                email = validated_data.get('email'),
                username = validated_data.get('username'),
                password = validated_data.get('password'),
                first_name = validated_data.get('first_name'),
                last_name = validated_data.get('last_name'),
            )
            user.set_password(validated_data.get('password'))
            user.save()
            return user


        # if user.has_perm('DaanpatraApp.can_add_drivers'):
        #     user = User.objects.create(
        #         email = validated_data.get('email'),
        #         username = validated_data.get('username'),
        #         password = validated_data.get('password'),
        #         name = validated_data.get('name'),
        #         birth_date = validated_data.get('birth_date'),
        #     )
        #     user.set_password(validated_data.get('password'))
        #     delete_perm = Permission.objects.get(codename='delete_user')
        #     view_perm = Permission.objects.get(codename='view_user')
        #     update_perm = Permission.objects.get(codename='change_user')
        #     user.user_permissions.add(view_perm, update_perm, delete_perm)
        #     user.save()
        #     return user
        # else:
        #     raise PermissionDenied()

#===========================================================================

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class DriverActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.has_perm('DaanpatraApp.can_update_drivers'):
            instance.name = validated_data.get('name', instance.name)
            instance.username = validated_data.get('username', instance.username)
            instance.email = validated_data.get('email', instance.email)
            instance.birth_date = validated_data.get('birth_date', instance.birth_date)
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.birth_date = validated_data.get('birth_date', instance.birth_date)
            instance.role = validated_data.get('role', instance.role)
            instance.save()
            if validated_data.get('password'):
                instance.set_password(validated_data.get('password'))
                instance.save()
            return instance
        else:
            raise PermissionDenied()


class UserActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.has_perm('DaanpatraApp.change_user'):
            instance.name = validated_data.get('name', instance.name)
            instance.username = validated_data.get('username', instance.username)
            instance.email = validated_data.get('email', instance.email)
            instance.birth_date = validated_data.get('birth_date', instance.birth_date)
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.birth_date = validated_data.get('birth_date', instance.birth_date)
            instance.role = validated_data.get('role', instance.role)
            instance.save()
            if validated_data.get('password'):
                instance.set_password(validated_data.get('password'))
                instance.save()
            return instance
        else:
            raise PermissionDenied()


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'

#==============================================================================

class DonationAccessSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        if self.context['request'].user.role == "Super_Admin":            
            data = Donation.objects.all()
            return super(DonationAccessSerializer, self).to_representation(data)
        else:
            raise serializers.ValidationError({"Message":"You're not authorized to view this page."})

class DonationSerializer(serializers.ModelSerializer):
    Product_Images = serializers.SerializerMethodField()
    class Meta:
        list_serializer_class = DonationAccessSerializer
        model = Donation
        fields = '__all__'

    def get_Product_Images(self, obj):
        return ProductImagesSerializer(ProductImages.objects.filter(donation=obj),many=True).data
    
#==============================================================================

# class FundDonationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FundDonation
#         fields = '__all__'

#================================================================================
class FilteredDonationSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = Donation.objects.filter(assign_to_sub_admin=self.context['request'].user.uuid)
        return super(FilteredDonationSerializer, self).to_representation(data)


class DonationActionsSerializer(serializers.ModelSerializer):
    Product_Images = ProductImagesSerializer(many=True)
    class Meta:
        list_serializer_class = FilteredDonationSerializer
        model = Donation
        fields = '__all__'

    def update(self, instance, validated_data):
        if self.context['request'].user.has_perm('DaanpatraApp.can_update_donation_status'):
            if self.context['request'].user.role == "Sub_Admin":
                data = Donation.objects.get(id=instance.id)
                if data.assign_to_sub_admin == self.context['request'].user:
                    instance.donation_status = validated_data.get('donation_status', instance.donation_status)
                    instance.save()
                    return instance
                else:
                    raise PermissionDenied
            else:
                instance.donation_status = validated_data.get('donation_status', instance.donation_status)
                instance.save()
                return instance
        else:
            raise PermissionDenied

#================================================================================

#-----------------------------TESTING PURPOSE-------------------------------

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'

class TranslateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'

class YouTubeVideoLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'

class GoogleLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'

#=============================================================================
class DonationGalleryViewSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        if self.context['request'].user.has_perm('DaanpatraApp.can_get_donation_gallery_images'):
            data = DonationGallery.objects.all()
            return super(DonationGalleryViewSerializer, self).to_representation(data)
        else:
            raise PermissionDenied()

class DonationGallerySerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = DonationGalleryViewSerializer
        model = DonationGallery
        fields = '__all__'

#=============================================================================

class UserAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserAppLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'


#-----------------------------TESTING PURPOSE-------------------------------