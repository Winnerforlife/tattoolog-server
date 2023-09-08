from django.contrib import admin

from apps.tools.models import SocialMedia, SocialMediaType


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    pass


@admin.register(SocialMediaType)
class SocialMediaTypeAdmin(admin.ModelAdmin):
    pass
