from typing import Optional

from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.accounts.models import Profile, CustomUser
from apps.tools.models import SocialMedia
from apps.tools.serializers import SocialMediaSerializer

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "first_name", "last_name", "password", "role")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "first_name", "last_name", "role")


class ProfileFilterSerializer(serializers.ModelSerializer):
    user = UserSerializer()
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
    user = UserSerializer()
    social_media_profile = SocialMediaSerializer(many=True)

    class Meta:
        model = Profile
        fields = (
            "user",
            "avatar",
            "salons_and_masters",
            "about",
            "status",
            "country",
            "city",
            "birthday",
            "phone_number",
            "social_media_profile"
        )

    def update(self, instance, validated_data):
        self.update_user(instance.user, validated_data.pop('user', None))
        self.update_social_media_profiles(instance, validated_data.pop('social_media_profile', []))
        instance = super().update(instance, validated_data)
        return instance

    def update_user(self, user, user_data):
        if user_data:
            for key, value in user_data.items():
                setattr(user, key, value)
            user.save()

    def update_social_media_profiles(self, instance, social_media_data):
        for social_media in social_media_data:
            social_media_type_name = social_media['social_media_type']['name']
            link = social_media['link']
            social_media_obj, created = SocialMedia.objects.get_or_create(
                profile=instance, social_media_type__name=social_media_type_name
            )
            social_media_obj.link = link
            social_media_obj.save()
