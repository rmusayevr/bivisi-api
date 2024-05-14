from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from .models import User, PhoneNumber, Subscription


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {
         'fields': ('first_name', 'last_name', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'avatar', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)


class PhoneNumberAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'phone', 'created_at', 'updated_at')
    search_fields = ('user__username', )
    list_filter = ('created_at', 'updated_at')


class SubscriptionAdmin(ImportExportModelAdmin):
    list_display = ('id', 'follower', 'follows', 'created_at', 'updated_at')
    search_fields = ('follower__username', 'follows__username')
    list_filter = ('created_at', 'updated_at')


admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
