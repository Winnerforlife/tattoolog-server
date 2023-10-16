from rest_framework import serializers
from cities_light.models import City, Country

from apps.tools.models import SocialMediaType, SocialMedia, Partners, Blog, Rating


class CountryCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name')


class CityCustomSerializer(serializers.ModelSerializer):
    country = CountryCustomSerializer()

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


class PartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partners
        fields = ('name', 'logo', 'link')


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
            'id',
            'image',
            'title',
            'body',
            'created_at',
            'slug',
            'meta_title_tag',
            'meta_description',
            'meta_keywords',
            'opengraph_title',
            'opengraph_description'
        )


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('profile', 'mark', 'comment')
