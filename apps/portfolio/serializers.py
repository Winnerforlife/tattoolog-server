from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from apps.portfolio.models import Post, Photo, WorkType


class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = ('id', 'name', 'description')


class PhotoSerializer(serializers.ModelSerializer):
    # photo = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Photo
        fields = ('photo',)


class PostSerializer(serializers.ModelSerializer):
    photo_post = PhotoSerializer(many=True, required=False)
    work_type = WorkTypeSerializer()

    class Meta:
        model = Post
        fields = ("id", "profile", "photo_post", "work_type", "description", "created_at")

    def create(self, validated_data):
        print(f"validated_data - {validated_data}")
        print(f"photo_post - {validated_data.pop('photo_post', [])}")
        photos_data = validated_data.pop('photo_post', [])
        print(f"photos_data - {photos_data}")
        post = Post.objects.create(**validated_data)
        for photo_data in photos_data:
            print(f"photo_data - {photo_data}")
            Photo.objects.create(post=post, **photo_data)
        return post
