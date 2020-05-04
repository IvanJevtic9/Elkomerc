from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import (Producer,
                     ProducerImage,
                     ProductGroup,
                     Attribute,
                     Article,
                     ArticleImage)

from .forms import (ProducerForm,
                    ProducerImageForm,
                    ProductGroupForm,
                    AttributeForm,
                    ArticleForm,
                    ArticleImageForm)

# Register your models here.

#list_filter

class ProducerAdmin(ImportExportModelAdmin):
    form = ProducerForm
    list_display = ('id', 'producer_name', 'link', 'description')
    fieldsets = (
        ("General info", {'fields': ('producer_name', 'link', 'description')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('producer_name', 'link', 'description'),
        }),
    )
    search_fields = ('id', 'producer_name', 'link', 'description',)
    ordering = ('id', 'producer_name', 'link', 'description',)

class ProducerImageAdmin(ImportExportModelAdmin):
    form = ProducerImageForm
    list_display = ('id', 'producer_id', 'image', 'image_name', 'purpose', 'content_type', 'size', 'height', 'width')
    fieldsets = (
        ("General info", {'fields': ('producer_id', 'image', 'image_name', 'purpose')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('producer_id', 'image', 'image_name', 'purpose',),
        }),
    )
    search_fields = ('id', 'producer_id', 'image', 'image_name', 'purpose', 'content_type', 'size', 'height', 'width',)
    ordering = ('id', 'producer_id', 'image', 'image_name', 'purpose', 'content_type', 'size', 'height', 'width',)

class AttributeAdmin(ImportExportModelAdmin):
    form = AttributeForm
    list_display = ('id', 'article_id', 'feature_id', 'value')
    list_filter = ('is_selectable',)
    fieldsets = (
        ("General info", {'fields': ('article_id', 'feature_id', 'value', 'is_selectable')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('article_id', 'feature_id', 'value', 'is_selectable'),
        }),
    )
    search_fields = ('id', 'article_id', 'feature_id', 'value', 'is_selectable',)
    ordering = ('id', 'article_id', 'feature_id', 'value', 'is_selectable',) 

class ArticleAdmin(ImportExportModelAdmin):
    form = ArticleForm
    list_display = ('id', 'article_name', 'sub_category_id', 'producer_id', 'product_group', 'description', 'price', 'unit_of_measure', 'currency', 'is_available')
    list_filter = ('is_available',)
    fieldsets = (
        ("General info", {'fields': ('article_name', 'sub_category_id', 'producer_id', 'product_group', 'description', 'price', 'unit_of_measure', 'currency', 'is_available')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('article_name', 'sub_category_id', 'producer_id', 'product_group', 'description', 'price', 'unit_of_measure', 'currency', 'is_available'),
        }),
    )
    search_fields = ('id', 'article_name', 'sub_category_id', 'producer_id', 'product_group', 'description', 'price', 'unit_of_measure', 'currency', 'is_available',)
    ordering = ('id', 'article_name', 'sub_category_id', 'producer_id', 'product_group', 'description', 'price', 'unit_of_measure', 'currency', 'is_available',) 

class ArticleImageAdmin(ImportExportModelAdmin):
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
admin.site.register(ProducerImage, ProducerImageAdmin)
admin.site.register(ProductGroup, ProductGroupFormAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleImage, ArticleImageAdmin)
