from django.contrib import admin

from .forms import CategoryForm, SubCategoryForm, FeatureForm, FloorFeatureForm
from .models import Category, SubCategory, Feature, FloorFeature

from import_export.admin import ImportExportModelAdmin

# Register your models here.

class CategoryAdmin(ImportExportModelAdmin):
    form = CategoryForm
    list_display = ('id', 'category_name')

    fieldsets = (
        ("General info", {'fields': ('category_name', )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'category_name'),
        }),
    )
    search_fields = ('id', 'category_name',)
    ordering = ('id', 'category_name',)

class SubCategoryAdmin(ImportExportModelAdmin):
    form = SubCategoryForm
    list_display = ('id', 'category_id', 'sub_category_name')

    fieldsets = (
        ("General info", {'fields': ('category_id', 'sub_category_name',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'category_id', 'sub_category_name'),
        }),
    )
    search_fields = ('id', 'category_id', 'sub_category_name',)
    ordering = ('id', 'category_id', 'sub_category_name',)

class FeatureAdmin(ImportExportModelAdmin):
    form = FeatureForm
    list_display = ('id', 'feature_name', 'data_type')
    list_filter = ('data_type', 'is_selectable',)

    fieldsets = (
        ("General info", {'fields': ('feature_name', 'data_type', 'is_selectable')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'feature_name', 'data_type', 'is_selectable',),
        }),
    )
    search_fields = ('id', 'feature_name', 'data_type',  'is_selectable',)
    ordering = ('id', 'feature_name', 'data_type',  'is_selectable',)

class FloorFeatureAdmin(ImportExportModelAdmin):
    form = FloorFeatureForm
    list_display = ('id', 'sub_category_id', 'feature_id',)

    fieldsets = (
        ("General info", {'fields': ('sub_category_id', 'feature_id',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'sub_category_id', 'feature_id'),
        }),
    )
    search_fields = ('id', 'sub_category_id', 'feature_id',)
    ordering = ('id', 'sub_category_id', 'feature_id',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(FloorFeature, FloorFeatureAdmin)    