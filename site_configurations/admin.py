from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Corosel
from .forms import CoroselForm

class CoroselAdmin(ImportExportModelAdmin):
    form = CoroselForm
    list_display = ('id', 'name', 'description', 'link',
                    'corosel_image', 'is_enabled')
    fieldsets = (
        ("General info", {'fields': ('name',
                                     'description',
                                     'link',
                                     'corosel_image',
                                     'is_enabled')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'description', 'link', 'corosel_image', 'is_enabled',)}),
    )
    search_fields = ('id', 'name', 'description', 'link',
                     'corosel_image', )
    ordering = ('id', 'name', 'description', 'link', 'is_enabled',)


admin.site.register(Corosel, CoroselAdmin)
