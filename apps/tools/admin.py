from django.contrib import admin

from apps.tools.models import SocialMedia, SocialMediaType, Partners


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    pass


@admin.register(SocialMediaType)
class SocialMediaTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    pass

