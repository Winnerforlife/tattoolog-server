from django.contrib import admin

from apps.portfolio.models import Post, Photo, WorkType, ModerationAssociation, AssociationPhotoProof, \
    ModerationFromProject


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkType)
class WorkType(admin.ModelAdmin):
    pass


class AssociationPhotoProofInline(admin.TabularInline):
    pk_name = 'moderation'
    model = AssociationPhotoProof
    extra = 0


@admin.register(ModerationAssociation)
class ModerationAssociationAdmin(admin.ModelAdmin):
    inlines = [AssociationPhotoProofInline]


@admin.register(ModerationFromProject)
class ModerationFromProjectAdmin(admin.ModelAdmin):
    pass
