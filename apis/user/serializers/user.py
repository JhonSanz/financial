
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk"]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username", "email", "password", "identification",
            "first_name"
        ]
    
    def create(self, validated_data):
        password = make_password(validated_data.pop("password"))
        user = User.objects.create(
            **validated_data,
            password=password
        )
        return user
