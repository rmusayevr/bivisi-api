from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from .models import User, PhoneNumber, Subscription


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {
            "fields": [
                "username",
                "email",
                "password",
            ]
        }),
        (_("Personal info"), {
            "fields": [
                "first_name",
                "last_name",
                "gender",
                "birthday",
                "avatar",
                "cover_image",
                "country",
                "sign_up_method"
            ]
        }),
        (_("Permissions"), {
            "fields": [
                "status",
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions"
            ]
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ["wide"],
            "fields": [
                "username",
                "email",
                "first_name",
                "last_name",
                "gender",
                "birthday",
                "country",
                "password1",
                "password2"
            ]
        }),
    )
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "sign_up_method",
        "gender",
        "birthday",
        "is_active",
        "status"
    ]
    list_filter = [
        "gender",
        "is_staff",
        "is_superuser",
        "is_active",
        "status",
        "groups",
        "sign_up_method",
    ]
    list_per_page = 15
    search_fields = [
        "username",
        "email",
        "first_name",
        "last_name",
        "gender",
        "sign_up_method"
    ]
    ordering = ["username"]
    filter_horizontal = ["groups", "user_permissions"]

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.avatar:
                obj.avatar.delete(save=False)

            if obj.cover_image:
                obj.cover_image.delete(save=False)

        # Call the delete_queryset method of the parent class
        super().delete_queryset(request, queryset)


class PhoneNumberAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "user",
        "phone",
        "created_at",
        "updated_at"
    ]
    list_display_links = ["user", "phone"]
    search_fields = ["user__username"]
    list_filter = ["created_at", "updated_at"]
    list_per_page = 15


class SubscriptionAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "follower",
        "follows",
        "created_at",
        "updated_at"
    ]
    list_display_links = ["follower"]
    search_fields = ["follower__username", "follows__username"]
    list_filter = ["created_at", "updated_at"]
    list_per_page = 15


admin.site.register(User, UserAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
