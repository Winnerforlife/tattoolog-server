from typing import Optional

from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.accounts.models import Profile

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "first_name", "last_name", "password", "role")


class ProfileFilterSerializer(serializers.ModelSerializer):
    user = CustomUserCreateSerializer()
    city = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ("user", "avatar", "salons_and_masters", "about", "status", "country", "city")

    def get_city(self, obj) -> Optional[str]:
        return obj.city.name if obj.city else None

    def get_country(self, obj) -> Optional[str]:
        return obj.country.name if obj.country else None


class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserCreateSerializer()

    class Meta:
        model = Profile
        fields = ("user", "avatar", "salons_and_masters", "about", "status", "country", "city")
