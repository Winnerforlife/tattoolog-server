from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.accounts.models import Profile

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "first_name", "last_name", "password", "role")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("user", "avatar", "salons_and_masters", "about", "status")
