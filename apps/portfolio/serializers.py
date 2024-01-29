from rest_framework import serializers

from apps.portfolio.models import Post, Photo, WorkType, ModerationAssociation, AssociationPhotoProof
from apps.tools.models import AssociationType
from apps.tools.serializers import AssociationTypeSerializer


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'post', 'photo')


class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = ('id', 'name', 'description', 'category')


class PostSerializer(serializers.ModelSerializer):
    photo_post = PhotoSerializer(many=True)
    work_type = WorkTypeSerializer()

    class Meta:
        model = Post
        fields = ("id", "profile", "work_type", "photo_post", "description", "created_at")


class PhotoCreateSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True)
    photos = serializers.ListField(child=serializers.ImageField(), write_only=True)

    class Meta:
        model = Photo
        fields = ('photos', 'post')
        extra_kwargs = {'photos': {'required': True}}

    def create(self, validated_data):
        photos_data = validated_data.pop("photos")
        post_photos = [
            Photo(photo=photo, **validated_data)
            for photo in photos_data
        ]
        return Photo.objects.bulk_create(post_photos)


class PostCreateSerializer(serializers.ModelSerializer):
    work_type = serializers.PrimaryKeyRelatedField(queryset=WorkType.objects.all(), required=False)

    class Meta:
        model = Post
        fields = ("id", "profile", "description", "work_type", "created_at")


class AssociationPhotoProofSerializer(serializers.ModelSerializer):
    moderation = serializers.PrimaryKeyRelatedField(queryset=ModerationAssociation.objects.all(), write_only=True)
    photos = serializers.ListField(child=serializers.ImageField(), write_only=True)

    class Meta:
        model = Photo
        fields = ('photos', 'moderation')
        extra_kwargs = {'photos': {'required': True}}

    def create(self, validated_data):
        photos_data = validated_data.pop("photos")
        post_photos = [
            AssociationPhotoProof(photo=photo, **validated_data)
            for photo in photos_data
        ]
        return AssociationPhotoProof.objects.bulk_create(post_photos)


class ModerationAssociationSerializer(serializers.ModelSerializer):
    # type = serializers.PrimaryKeyRelatedField(queryset=AssociationType.objects.all(), required=False)
    type = AssociationTypeSerializer()

    class Meta:
        model = ModerationAssociation
        fields = ("id", "profile", "type", "status", "comment")
