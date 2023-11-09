from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.tools.models import SocialMedia, SocialMediaType, Partners, Blog, Rating, AssociationType, Festival


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    pass


@admin.register(SocialMediaType)
class SocialMediaTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    pass


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Blog'), {'fields': ('image', 'title', 'body', 'created_at')}),
        (_('SEO Meta'), {'fields': (
            'slug', 'meta_title_tag', 'meta_description', 'meta_keywords', 'opengraph_title', 'opengraph_description'
            )
        }),
    )


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass


@admin.register(AssociationType)
class AssociationTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    pass
