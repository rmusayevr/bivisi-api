from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import FAQ, Slider


class SliderAdmin(ImportExportModelAdmin):
    list_display = ['id', 'image', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.image:
                obj.image.delete(save=False)
        super().delete_queryset(request, queryset)


class FAQAdmin(ImportExportModelAdmin):
    # fieldsets = (
    #     ('EN', {'fields': ('faq_en', 'answer_en')}),  # English fields
    #     ('AZ', {'fields': ('faq_az', 'answer_az')}),  # Azerbaijani fields
    #     ('TR', {'fields': ('faq_tr', 'answer_tr')}),  # Turkish fields
    #     ('RU', {'fields': ('faq_ru', 'answer_ru')}),  # Russian fields
    #     ('Additional', {'fields': ('is_active', )}),  # Non-translated fields
    # )
    list_display = ['id', 'faq', 'answer', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'faq']
    list_filter = ['is_active']
    search_fields = ['faq']


admin.site.register(FAQ, FAQAdmin)
admin.site.register(Slider, SliderAdmin)
