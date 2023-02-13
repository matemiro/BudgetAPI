from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from utils import pop_null_values_from_dict

UserModel = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user

    class Meta:
        model = UserModel
        fields = ("id", "username", "password", "email")

    def validate_email(self, email):
        """
        Email must be unique or empty string ("").
        """
        if (not email == "") and UserModel.objects.filter(email=email):
            raise ValidationError("User with given email already exist.")
        return email


class UserUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("username",)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "email",
        )

    def to_representation(self, instance):
        """
        Return only not null values.
        """
        representation = super().to_representation(instance)
        return pop_null_values_from_dict(representation)
