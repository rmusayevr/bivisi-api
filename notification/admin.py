from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Notification


class NotificationAdmin(ImportExportModelAdmin):
    list_display = [
        "__str__",
        "is_read",
        "created_at",
        "updated_at"
    ]
    list_filter = [
        "is_read",
        "recipient__username",  # Optimize filtering by using related field's specific attribute
        "sender__username",     # Same as above for sender
        "created_at",
        "updated_at"
    ]
    search_fields = [
        "recipient__username",  # Add search functionality for recipient username
        "sender__username",     # Add search functionality for sender username
        "message",              # Allow searching by message content
    ]
    list_select_related = ["recipient", "sender"]  # Optimize query with select_related
    list_per_page = 20  # Increase items per page for better navigation


admin.site.register(Notification, NotificationAdmin)
