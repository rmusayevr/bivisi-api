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
        "recipient",
        "sender",
        "created_at",
        "updated_at"
    ]
    list_per_page = 15


admin.site.register(Notification, NotificationAdmin)
