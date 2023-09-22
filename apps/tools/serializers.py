from rest_framework import serializers
from cities_light.models import City, Country

from apps.accounts.models import Profile
from apps.accounts.serializers import UserSerializer
from apps.portfolio.serializers import PostSerializer
from apps.tools.models import SocialMediaType, SocialMedia


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name')


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = City
        fields = ('id', 'name', 'country')


class SocialMediaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaType
        fields = ('name',)


class SocialMediaSerializer(serializers.ModelSerializer):
    social_media_type = SocialMediaTypeSerializer()

    class Meta:
        model = SocialMedia
        fields = ('social_media_type', 'link')


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
    user = UserSerializer()
    social_media_profile = SocialMediaSerializer(many=True)
    post_profile = PostSerializer(many=True)

    class Meta:
        model = Profile
        fields = ('user', 'post_profile', 'about', 'social_media_profile', 'phone_number')

    def to_representation(self, instance):
        data = super().to_representation(instance)

        all_photos = []
        for post_data in data['post_profile']:
            all_photos.extend(post_data.pop('photo_post', []))

        data['post_profile'] = all_photos

        return data
