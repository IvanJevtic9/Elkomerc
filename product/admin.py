from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import (Producer,
                     ProducerImage,
                     Program,
                     Product,
                     Attribute,
                     Article,
                     ArticleImage)

from .forms import (ProducerForm,
                    ProducerImageForm,
                    ProgramForm,
                    ProductForm,
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
    list_display = ('id', 'producer_id', 'image', 'image_name', 'content_type', 'size', 'height', 'width')
    fieldsets = (
        ("General info", {'fields': ('producer_id', 'image', 'image_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('producer_id', 'image', 'image_name'),
        }),
    )
    search_fields = ('id', 'producer_id', 'image', 'image_name', 'content_type', 'size', 'height', 'width',)
    ordering = ('id', 'producer_id', 'image', 'image_name', 'content_type', 'size', 'height', 'width',)

class ProgramAdmin(ImportExportModelAdmin):
    form = ProgramForm
    list_display = ('id', 'program_name', 'producer_id')
    fieldsets = (
        ("General info", {'fields': ('program_name', 'producer_id')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('program_name', 'producer_id'),
        }),
    )
    search_fields = ('id', 'program_name', 'producer_id',)
    ordering = ('id', 'program_name', 'producer_id',) 

class ProductAdmin(ImportExportModelAdmin):
    form = ProductForm
    list_display = ('id', 'product_name', 'sub_category_id', 'description', 'unit_of_measure')
    fieldsets = (
        ("General info", {'fields': ('product_name', 'sub_category_id', 'description', 'unit_of_measure')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('product_name', 'sub_category_id', 'description', 'unit_of_measure'),
        }),
    )
    search_fields = ('id', 'product_name', 'sub_category_id', 'description', 'unit_of_measure',)
    ordering = ('id', 'product_name', 'sub_category_id', 'description', 'unit_of_measure',) 

class AttributeAdmin(ImportExportModelAdmin):
    form = AttributeForm
    list_display = ('id', 'product_id', 'feature_id', 'value')
    fieldsets = (
        ("General info", {'fields': ('product_id', 'feature_id', 'value')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('product_id', 'feature_id', 'value'),
        }),
    )
    search_fields = ('id', 'product_id', 'feature_id', 'value',)
    ordering = ('id', 'product_id', 'feature_id', 'value',) 

class ArticleAdmin(ImportExportModelAdmin):
    form = ArticleForm
    list_display = ('id', 'product_id', 'program_id', 'price', 'currency', 'is_available')
    fieldsets = (
        ("General info", {'fields': ('product_id', 'program_id', 'price', 'currency', 'is_available')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('product_id', 'program_id', 'price', 'currency', 'is_available'),
        }),
    )
    search_fields = ('id', 'product_id', 'program_id', 'price', 'currency', 'is_available',)
    ordering = ('id', 'product_id', 'program_id', 'price', 'currency', 'is_available',) 

class ArticleImageAdmin(ImportExportModelAdmin):
    form = ArticleImageForm
    list_display = ('id', 'article_id', 'image', 'image_name', 'content_type', 'size', 'height', 'width')
    fieldsets = (
        ("General info", {'fields': ('article_id', 'image', 'image_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('article_id', 'image', 'image_name'),
        }),
    )
    search_fields = ('id', 'article_id', 'image', 'image_name', 'content_type', 'size', 'height', 'width',)
    ordering = ('id', 'article_id', 'image', 'image_name', 'content_type', 'size', 'height', 'width',) 

admin.site.register(Producer, ProducerAdmin)
admin.site.register(ProducerImage, ProducerImageAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleImage, ArticleImageAdmin)
