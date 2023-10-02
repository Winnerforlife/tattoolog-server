from django.contrib import admin

from apps.portfolio.models import Post, Photo, WorkType


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkType)
class WorkType(admin.ModelAdmin):
    pass
