from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import (Producer,
                     ProductGroup,
                     Attribute,
                     Article,
                     ArticleImage,
                     PaymentItem,
                     PaymentOrder)

from .forms import (ProducerForm,
                    ProductGroupForm,
                    AttributeForm,
                    ArticleForm,
                    ArticleImageForm,
                    PaymentItemForm,
                    PaymentOrderForm)

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
    search_fields = ('id', 'article_id__article_name', 'feature_id__feature_name',)
    ordering = ('id', 'article_id__article_name', 'feature_id__feature_name', 'value',) 

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
    search_fields = ('id', 'article_code', 'article_name', 'sub_category_id__sub_category_name', 'producer_id__producer_name', 'product_group_id__group_name', 'description', 'unit_of_measure',)
    ordering = ('id', 'article_code', 'article_name', 'sub_category_id__sub_category_name', 'producer_id__producer_name', 'product_group_id__group_name', 'description', 'price', 'unit_of_measure', 'currency', 'is_available',) 

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
    search_fields = ('id', 'article_id__article_name', 'image', 'image_name', 'purpose', 'content_type',)
    ordering = ('id', 'article_id__article_name', 'image', 'image_name', 'purpose', 'content_type', 'size', 'height', 'width',) 

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

class PaymentItemAdmin(admin.ModelAdmin):
    form = PaymentItemForm
    readonly_fields = ('user_discount', 'article_price')
    list_display = ('id', 'article_id', 'payment_order_id', 'amount', 'user_discount', 'article_price')
    fieldsets = (
        ("General info", {'fields': ('article_id', 'payment_order_id', 'number_of_pieces', 'user_discount', 'article_price',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('article_id', 'payment_order_id', 'number_of_pieces', 'user_discount', 'article_price',),
        }),
    )
    search_fields = ('id', 'article_id__article_name', 'payment_order_id__email__email',)
    ordering = ('id', 'article_id__article_name', 'payment_order_id__email', 'user_discount', 'article_price',) 

class PaymentOrderAdmin(admin.ModelAdmin):
    form = PaymentOrderForm
    readonly_fields = ('attribute_notes',)
    list_display = ('id', 'email', 'note', 'attribute_notes', 'method_of_payment', 'status')
    list_filter = ('status',)
    fieldsets = (
        ("General info", {'fields': ('email', 'note', 'method_of_payment', 'status',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'note', 'method_of_payment', 'status',),
        }),
    )
    search_fields = ('id', 'email__email', 'method_of_payment', 'status',)
    ordering = ('id', 'email__email', 'note', 'attribute_notes', 'method_of_payment', 'status',) 

admin.site.register(Producer, ProducerAdmin)
admin.site.register(ProductGroup, ProductGroupFormAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleImage, ArticleImageAdmin)
admin.site.register(PaymentItem, PaymentItemAdmin)
admin.site.register(PaymentOrder, PaymentOrderAdmin)
