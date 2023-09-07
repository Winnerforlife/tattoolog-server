from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from apps.portfolio.models import Post, Photo


class PhotoSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)

    class Meta:
        model = Photo
        fields = ('id', 'post', 'photo')


class PostSerializer(serializers.ModelSerializer):
    photo_post = PhotoSerializer(many=True, required=True)

    class Meta:
        model = Post
        fields = ("id", "profile", "photo_post", "description", "work_type", "created_at")

    def create(self, validated_data):
        photos_data = validated_data.pop('photo_post', [])
        post = Post.objects.create(**validated_data)

        for photo_data in photos_data:
            if 'photo' in photo_data:
                Photo.objects.create(post=post, **photo_data)

        return post

    # def create(self, validated_data):
    #     images_data = validated_data.pop("photo_post")
    #     post_photos = [
    #         Post(
    #             image=image, **validated_data
    #         )
    #         for image in images_data
    #     ]
    #     return Post.objects.bulk_create(post_photos)
