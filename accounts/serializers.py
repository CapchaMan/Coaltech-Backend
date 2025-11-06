from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Vendor, Product


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_vendor', 'is_rider']


class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Vendor
        fields = ['id', 'user', 'business_name', 'business_address', 'business_phone', 'business_email', 'business_description', 'profile_picture', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'vendor', 'name', 'description', 'price', 'image', 'created_at']
