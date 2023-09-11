from rest_framework import serializers

from apps.portfolio.models import Post, Photo, WorkType


class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = ('id', 'name', 'description')


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('photo',)


class PostSerializer(serializers.ModelSerializer):
    photo_post = PhotoSerializer(many=True, required=False)
    work_type = WorkTypeSerializer()

    class Meta:
        model = Post
        fields = ("id", "profile", "photo_post", "description", "work_type", "created_at")
