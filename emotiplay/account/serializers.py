from rest_framework import serializers
from django.contrib.auth import get_user_model
from video.models import Category
from djoser.serializers import TokenSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "date_of_birth",
            "email",
            "phone_number",
            "gender",
            "preferences",
            "role",
        ]
        read_only_fields = ["role"]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "email",
            "phone_number",
            "gender",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AdminCreateSerializer(UserCreateSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.role = "admin"
        user.is_staff = True
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "preferences", "gender"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "name"]


class CustomTokenSerializer(TokenSerializer):
    user = serializers.SerializerMethodField()

    class Meta(TokenSerializer.Meta):
        fields = ("auth_token", "user")

    def get_user(self, obj):
        user = obj.user
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_of_birth": user.date_of_birth,
            "email": user.email,
            "phone_number": user.phone_number,
            "gender": user.gender,
            "role": user.role,
            "date_joined": user.date_joined,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "preferences": [category.id for category in user.preferences.all()],
        }
