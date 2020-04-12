from django.contrib import admin

from .forms import CategoryForm, SubCategoryForm, FeatureForm, FloorFeatureForm
from .models import Category, SubCategory, Feature, FloorFeature
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ('category_id', 'category_name')

    fieldsets = (
        ("General info", {'fields': ('category_name', )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('category_id', 'category_name'),
        }),
    )
    search_fields = ('category_id', 'category_name',)
    ordering = ('category_id', 'category_name',)

class SubCategoryAdmin(admin.ModelAdmin):
    form = SubCategoryForm
    list_display = ('sub_category_id', 'category_id', 'sub_category_name')

    fieldsets = (
        ("General info", {'fields': ('category_id', 'sub_category_name',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('sub_category_id', 'category_id', 'sub_category_name'),
        }),
    )
    search_fields = ('sub_category_id', 'category_id', 'sub_category_name',)
    ordering = ('sub_category_id', 'category_id', 'sub_category_name',)

class FeatureAdmin(admin.ModelAdmin):
    form = FeatureForm
    list_display = ('feature_id', 'feature_name', 'data_type')
    list_filter = ('data_type',)

    fieldsets = (
        ("General info", {'fields': ('feature_name', 'data_type',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('feature_id', 'feature_name', 'data_type'),
        }),
    )
    search_fields = ('feature_id', 'feature_name', 'data_type',)
    ordering = ('feature_id', 'feature_name', 'data_type',)

class FloorFeatureAdmin(admin.ModelAdmin):
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