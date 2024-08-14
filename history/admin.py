from django.contrib import admin
from .models import UserHistory
from import_export.admin import ImportExportModelAdmin


class UserHistoryAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "user",
        "product_video_type",
        "watch_date",
        "created_at",
        "updated_at"
    ]
    list_display_links = ["id", "user"]
    list_filter = [
        "user__username",
        "watch_date",
        "created_at",
        "updated_at"
    ]
    list_per_page = 15
    search_fields = ["user__username"]
    readonly_fields = ["created_at", "updated_at"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'product_video_type')


admin.site.register(UserHistory, UserHistoryAdmin)
