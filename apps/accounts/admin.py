from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Profile, CustomUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('country', 'city')
    fields = ('avatar', 'salons_and_masters', 'about', 'status', 'country', 'city', 'birthday', 'phone_number')


@admin.register(CustomUser)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'role')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_admin',)
    list_filter = ('is_active', 'is_staff', 'is_admin',)
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)
    filter_horizontal = ()
