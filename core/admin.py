from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import FAQ, Slider, Stream


class SliderAdmin(ImportExportModelAdmin):
    list_display = ["__str__", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    list_per_page = 15

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.image:
                obj.image.delete(save=False)
        super().delete_queryset(request, queryset)


class FAQAdmin(ImportExportModelAdmin):
    # fieldsets = (
    #     ("EN", {"fields": ("faq_en", "answer_en")}),  # English fields
    #     ("AZ", {"fields": ("faq_az", "answer_az")}),  # Azerbaijani fields
    #     ("TR", {"fields": ("faq_tr", "answer_tr")}),  # Turkish fields
    #     ("RU", {"fields": ("faq_ru", "answer_ru")}),  # Russian fields
    #     ("Additional", {"fields": ("is_active", )}),  # Non-translated fields
    # )
    list_display = ["__str__", "is_active", "created_at", "updated_at"]
    list_display_links = ["__str__"]
    list_filter = ["is_active"]
    list_per_page = 15
    search_fields = ["faq"]


class StreamAdmin(ImportExportModelAdmin):
    list_display = [
        "room_id",
        "room_name",
        "user_name",
        "product",
        "created_at",
        "updated_at"
    ]
    list_display_links = ["room_id", "room_name"]
    list_filter = ["user_name", "product", "created_at", "updated_at"]
    list_per_page = 15


admin.site.register(FAQ, FAQAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Stream, StreamAdmin)
