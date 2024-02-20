from rest_framework import serializers
from cities_light.models import City, Country


from apps.tools.models import (SocialMediaType, SocialMedia, Partners, Rating, AssociationType, Festival, BlogBodyPhoto,
                               BlogBody, BlogMeta, BlogPost, BlogPhotoCarousel, BlogCategory, FestivalCategory, Project,
                               FestivalPhotoSubmission, FestivalPhotoVote)


class CountryCustomSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        model = Country
        fields = ('id', 'name')


class CityCustomSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        model = City
        fields = ('id', 'name')


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
        fields = ('name', 'logo', 'link', 'type')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('profile', 'mark', 'comment')


class AssociationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssociationType
        fields = ('id', 'name', 'link')


class FestivalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FestivalCategory
        fields = ('id', 'name')


class FestivalPhotoSubmissionSerializer(serializers.ModelSerializer):
    votes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FestivalPhotoSubmission
        fields = ('id', 'image', 'votes_count')

    @staticmethod
    def get_votes_count(obj):
        """
        Возвращает количество голосов для фотографии.
        """
        return FestivalPhotoVote.objects.filter(photo_submission=obj).count()


class FestivalSerializer(serializers.ModelSerializer):
    category = FestivalCategorySerializer(read_only=True)
    photo_submissions = serializers.SerializerMethodField()

    class Meta:
        model = Festival
        fields = (
            'id',
            'image',
            'title',
            'category',
            'about_en', 'about_uk', 'about_pl', 'about_de',
            'rules_en', 'rules_uk', 'rules_pl', 'rules_de',
            'slug',
            'date_end',
            'created_at',
            'form_url',
            'country',
            'photo_submissions'
        )

    def get_photo_submissions(self, obj):
        """
        Фильтруем photo_submissions, чтобы возвращать только те, которые имеют статус 'approved'.
        """
        approved_submissions = FestivalPhotoSubmission.objects.filter(festival=obj, status='approved')
        return FestivalPhotoSubmissionSerializer(approved_submissions, many=True, context=self.context).data


class FestivalPhotoSubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FestivalPhotoSubmission
        fields = ('festival', 'image')


class FestivalPhotoVoteSerializer(serializers.ModelSerializer):
    voter_ip = serializers.IPAddressField(read_only=True)

    class Meta:
        model = FestivalPhotoVote
        fields = ('id', 'photo_submission', 'voted_at', 'voter_ip')
        read_only_fields = ('voted_at',)


class BlogBodyPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogBodyPhoto
        fields = ('photo', 'alt_name')


class BlogBodySerializer(serializers.ModelSerializer):
    blog_body_photo = BlogBodyPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = BlogBody
        fields = ('title', 'body', 'blog_body_photo')


class BlogMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogMeta
        fields = ('meta_title_tag', 'meta_description', 'meta_keywords',
                  'opengraph_title', 'opengraph_description', 'opengraph_image')


class BlogPhotoCarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPhotoCarousel
        fields = ('photo',)


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ('id', 'name')


class BlogPostSerializer(serializers.ModelSerializer):
    blog_body = BlogBodySerializer(many=True, read_only=True)
    blog_meta = BlogMetaSerializer(read_only=True)
    blog_photo_carousel = BlogPhotoCarouselSerializer(many=True, read_only=True)
    category = BlogCategorySerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = (
            'id',
            'category',
            'language',
            'country',
            'image',
            'title',
            'created_at',
            'slug',
            'blog_body',
            'blog_meta',
            'blog_photo_carousel',
            'is_active'
        )


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'link')
