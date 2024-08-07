import nested_admin
import admin_thumbnails

from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin
from django.contrib import admin

from apps.tools.choices import LANGUAGE_CHOICE
from apps.tools.models import (SocialMedia, SocialMediaType, Partners, Rating, AssociationType, Festival, BlogPost,
                               BlogBody, BlogBodyPhoto, BlogMeta, BlogPhotoCarousel, BlogCategory, FestivalCategory,
                               Project)


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    pass


@admin.register(SocialMediaType)
class SocialMediaTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    pass


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass


@admin.register(AssociationType)
class AssociationTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Festival)
class FestivalAdmin(TabbedTranslationAdmin):
    pass


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    pass


@admin_thumbnails.thumbnail('photo')
class BlogBodyPhotoInline(nested_admin.NestedTabularInline):
    model = BlogBodyPhoto
    extra = 1


class BlogBodyInline(nested_admin.NestedStackedInline):
    model = BlogBody
    extra = 0
    inlines = [BlogBodyPhotoInline]


@admin_thumbnails.thumbnail('opengraph_image')
class BlogMetaInline(nested_admin.NestedStackedInline):
    model = BlogMeta
    extra = 0


@admin_thumbnails.thumbnail('photo')
class BlogPhotoCarouselInline(nested_admin.NestedTabularInline):
    model = BlogPhotoCarousel
    extra = 0


@admin.register(BlogPost)
class BlogPostAdmin(nested_admin.NestedModelAdmin):
    inlines = [BlogBodyInline, BlogMetaInline, BlogPhotoCarouselInline]
    readonly_fields = ('language',)
    list_filter = ('country',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.save()
            slug = obj.slug

            for lang_code, lang_name in LANGUAGE_CHOICE:
                if lang_code != obj.language:
                    BlogPost.objects.create(
                        slug=slug,
                        country=obj.country,
                        language=lang_code,
                    )
        else:
            obj.save()


@admin.register(FestivalCategory)
class FestivalCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
