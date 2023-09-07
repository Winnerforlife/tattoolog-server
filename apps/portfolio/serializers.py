from rest_framework import serializers

from apps.portfolio.models import Post, Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('photo',)


class PostSerializer(serializers.ModelSerializer):
    photo_post = PhotoSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ("id", "profile", "photo_post", "description", "work_type", "created_at")
