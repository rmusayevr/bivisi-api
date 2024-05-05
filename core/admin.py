from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Slider


class SliderAdmin(ImportExportModelAdmin):
    list_display = ['id', 'image', 'created_at', 'updated_at']

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.image:
                storage, path = obj.image.storage, obj.image.path
                storage.delete(path)

        # Call the delete_queryset method of the parent class
        super().delete_queryset(request, queryset)


admin.site.register(Slider, SliderAdmin)