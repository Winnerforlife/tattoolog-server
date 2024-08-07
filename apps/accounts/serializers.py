from typing import Optional
from cities_light.models import Country, City
from phonenumber_field.serializerfields import PhoneNumberField
from django.db.models import Avg
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.accounts.models import Profile, CustomUser
from apps.portfolio.models import ModerationAssociation, ModerationFromProject
from apps.portfolio.serializers import PostSerializer, ProfileFromProjectSerializer, ProfileAssociationSerializer
from apps.tools.models import SocialMedia, Rating
from apps.tools.serializers import SocialMediaSerializer, CityCustomSerializer, CountryCustomSerializer

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "first_name", "last_name", "password", "role")

#TODO: phone_number
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "first_name", "last_name", "role")


class ProfileFilterSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    city = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    rating = serializers.ReadOnlyField(source='get_average_rating')
    moderation_profile_associate = serializers.SerializerMethodField()
    moderation_profile_from_project = serializers.SerializerMethodField()

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
            "rating",
            "open_to_work",
            'mentor',
            'relocate',
            "trusted_mentor",
            "posted_in_journal",
            'moderation_profile_associate',
            'moderation_profile_from_project',
        )

    def get_city(self, obj) -> Optional[str]:
        return obj.city.name if obj.city else None

    def get_country(self, obj) -> Optional[str]:
        return obj.country.name if obj.country else None

    def get_moderation_profile_associate(self, obj):
        moderation_items = ModerationAssociation.objects.filter(profile=obj, status='approved')
        return ProfileAssociationSerializer(moderation_items, many=True).data

    def get_moderation_profile_from_project(self, obj):
        moderation_items = ModerationFromProject.objects.filter(profile=obj, status='approved')
        return ProfileFromProjectSerializer(moderation_items, many=True).data


class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    social_media_profile = SocialMediaSerializer(many=True)
    rating = serializers.ReadOnlyField(source='get_average_rating')
    country = CountryCustomSerializer()
    city = CityCustomSerializer()
    moderation_profile_associate = ProfileAssociationSerializer(many=True, read_only=True)
    moderation_profile_from_project = ProfileFromProjectSerializer(many=True, read_only=True)

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
            "address",
            "birthday",
            "social_media_profile",
            "count_visit",
            "rating",
            "moderation_profile_associate",
            "open_to_work",
            "mentor",
            "relocate",
            "trusted_mentor",
            "posted_in_journal",
            "moderation_profile_from_project",
        )

    def update(self, instance, validated_data):
        self.update_user(instance.user, validated_data.pop('user', None))
        self.update_social_media_profiles(instance, validated_data.pop('social_media_profile', []))
        self.update_country(instance, validated_data.pop('country', None))
        self.update_city(instance, validated_data.pop('city', None))

        instance = super().update(instance, validated_data)
        return instance

    def update_user(self, user, user_data):
        if user_data:
            for key, value in user_data.items():
                setattr(user, key, value)
            user.save()

    def update_country(self, instance, country_data):
        if country_data:
            country_name = country_data.get('name')
            country_id = country_data.get('id')
            country = Country.objects.get(name=country_name, id=country_id)
            instance.country = country

    def update_city(self, instance, city_data):
        if city_data:
            city_name = city_data.get('name')
            city_id = city_data.get('id')
            city = City.objects.get(name=city_name, id=city_id)
            instance.city = city

    def update_social_media_profiles(self, instance, social_media_data):
        for social_media in social_media_data:
            social_media_type_name = social_media['social_media_type']['name']
            link = social_media['link']
            social_media_obj, created = SocialMedia.objects.get_or_create(
                profile=instance, social_media_type__name=social_media_type_name
            )
            social_media_obj.link = link
            social_media_obj.save()


class CRMIntegrationProfiles(serializers.ModelSerializer):
    """
        Сериализатор для данных которые будут переданы в ЦРМ, для создания кандидата

        first_name
        last_name
        email
        images
        about_candidate
        social_media_link
        phone
    """
    user = CustomUserSerializer()
    social_media_profile = SocialMediaSerializer(many=True)
    post_profile = PostSerializer(many=True)

    class Meta:
        model = Profile
        fields = ('user', 'post_profile', 'about', 'social_media_profile')

    def to_representation(self, instance):
        data = super().to_representation(instance)

        all_photos = []
        for post_data in data['post_profile']:
            all_photos.extend(post_data.pop('photo_post', []))

        data['post_profile'] = all_photos

        return data


class TransferActivationEmailSerializer(serializers.Serializer):
    """
        Сериализатор для данных которые приходят из CRM
    """
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    role = serializers.CharField(required=True)
    email = serializers.EmailField(required=False)
    phone_number = PhoneNumberField(required=False)
    about = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    social_link = serializers.CharField(required=False)
    avatar = serializers.ImageField(required=False)
    work_photos = serializers.ListField(
        child=serializers.ImageField(), required=False
    )
