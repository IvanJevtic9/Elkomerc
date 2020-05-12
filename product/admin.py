from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import (Producer,
                     ProductGroup,
                     Attribute,
                     Article,
                     ArticleImage)

from .forms import (ProducerForm,
                    ProductGroupForm,
                    AttributeForm,
                    ArticleForm,
                    ArticleImageForm)

# Register your models here.

#list_filter

class ProducerAdmin(ImportExportModelAdmin):
    form = ProducerForm
    list_display = ('id', 'producer_name', 'link', 'profile_image', 'description')
    fieldsets = (
        ("General info", {'fields': ('producer_name', 'link', 'profile_image', 'description')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('producer_name', 'link', 'profile_image', 'description'),
        }),
    )
    search_fields = ('id', 'producer_name', 'link', 'profile_image', 'description',)
    ordering = ('id', 'producer_name', 'link', 'profile_image', 'description',)

class AttributeAdmin(ImportExportModelAdmin):
    form = AttributeForm
    list_display = ('id', 'article_id', 'feature_id', 'value')
    fieldsets = (
        ("General info", {'fields': ('article_id', 'feature_id', 'value',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('article_id', 'feature_id', 'value',),
        }),
    )
    search_fields = ('id', 'article_id', 'feature_id', 'value',)
    ordering = ('id', 'article_id', 'feature_id', 'value',) 

class ArticleAdmin(ImportExportModelAdmin):
    form = ArticleForm
    list_display = ('id', 'article_code', 'article_name', 'sub_category_id', 'producer_id', 'product_group_id', 'description', 'price', 'unit_of_measure', 'currency', 'is_available')
    list_filter = ('is_available',)
    fieldsets = (
        ("General info", {'fields': ('article_code', 'article_name', 'sub_category_id', 'producer_id', 'product_group_id', 'description', 'price', 'unit_of_measure', 'currency', 'is_available')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('article_code', 'article_name', 'sub_category_id', 'producer_id', 'product_group_id', 'description', 'price', 'unit_of_measure', 'currency', 'is_available'),
        }),
    )
    search_fields = ('id', 'article_code', 'article_name', 'sub_category_id', 'producer_id', 'product_group_id', 'description', 'price', 'unit_of_measure', 'currency', 'is_available',)
    ordering = ('id', 'article_code', 'article_name', 'sub_category_id', 'producer_id', 'product_group_id', 'description', 'price', 'unit_of_measure', 'currency', 'is_available',) 

class ArticleImageAdmin(admin.ModelAdmin):
    form = ArticleImageForm
    list_display = ('id', 'article_id', 'image', 'image_name', 'purpose', 'content_type', 'size', 'height', 'width')
    fieldsets = (
        ("General info", {'fields': ('article_id', 'image', 'image_name', 'purpose',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('article_id', 'image', 'image_name', 'purpose',),
        }),
    )
    search_fields = ('id', 'article_id', 'image', 'image_name', 'purpose', 'content_type', 'size', 'height', 'width',)
    ordering = ('id', 'article_id', 'image', 'image_name', 'purpose', 'content_type', 'size', 'height', 'width',) 

class ProductGroupFormAdmin(ImportExportModelAdmin):
    form = ProductGroupForm
    list_display = ('id', 'group_name')
    fieldsets = (
        ("General info", {'fields': ('group_name',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('group_name',),
        }),
    )
    search_fields = ('id', 'group_name',)
    ordering = ('id', 'group_name',) 


admin.site.register(Producer, ProducerAdmin)
admin.site.register(ProductGroup, ProductGroupFormAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleImage, ArticleImageAdmin)
