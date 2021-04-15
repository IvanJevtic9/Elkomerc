from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import (Producer,
                     ProductGroup,
                     Attribute,
                     Article,
                     ArticleImage,
                     PaymentItem,
                     PaymentOrder,
                     PaymentOrderCommentHistory,
                     ArticleGroup)

from .forms import (ProducerForm,
                    ProductGroupForm,
                    AttributeForm,
                    ArticleForm,
                    ArticleImageForm,
                    PaymentItemForm,
                    PaymentOrderForm,
                    PaymentOrderCommentHistoryForm,
                    ArticleGroupForm)


class ProducerAdmin(ImportExportModelAdmin):
    form = ProducerForm
    list_display = ('id', 'producer_name', 'link',
                    'profile_image', 'description')
    fieldsets = (
        ("General info", {'fields': ('producer_name',
                                     'link', 'profile_image', 'description')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('producer_name', 'link', 'profile_image', 'description'),
        }),
    )
    search_fields = ('id', 'producer_name', 'link',
                     'profile_image', 'description',)
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
    search_fields = ('id', 'article_id__article_name',
                     'feature_id__feature_name',)
    ordering = ('id', 'article_id__article_name',
                'feature_id__feature_name', 'value',)


class ArticleAdmin(ImportExportModelAdmin):
    form = ArticleForm
    list_display = ('id', 'article_code', 'article_name', 'sub_category_id', 'producer_id',
                    'product_group_id', 'description', 'price', 'unit_of_measure', 'currency', 'is_available')
    list_filter = ('is_available',)
    fieldsets = (
        ("General info", {'fields': ('article_code', 'article_name', 'sub_category_id', 'producer_id',
                                     'product_group_id', 'description', 'price', 'unit_of_measure', 'currency', 'is_available')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('article_code', 'article_name', 'sub_category_id', 'producer_id', 'product_group_id', 'description', 'price', 'unit_of_measure', 'currency', 'is_available'),
        }),
    )
    search_fields = ('id', 'article_code', 'article_name', 'sub_category_id__sub_category_name',
                     'producer_id__producer_name', 'product_group_id__group_name', 'description', 'unit_of_measure',)
    ordering = ('id', 'article_code', 'article_name', 'sub_category_id__sub_category_name', 'producer_id__producer_name',
                'product_group_id__group_name', 'description', 'price', 'unit_of_measure', 'currency', 'is_available',)


class ArticleImageAdmin(admin.ModelAdmin):
    form = ArticleImageForm
    list_display = ('id', 'article_id', 'image', 'image_name',
                    'purpose', 'content_type', 'size', 'height', 'width')
    fieldsets = (
        ("General info", {'fields': ('article_id',
                                     'image', 'image_name', 'purpose',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('article_id', 'image', 'image_name', 'purpose',),
        }),
    )
    search_fields = ('id', 'article_id__article_name', 'image',
                     'image_name', 'purpose', 'content_type',)
    ordering = ('id', 'article_id__article_name', 'image', 'image_name',
                'purpose', 'content_type', 'size', 'height', 'width',)


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
    list_display = ('id', 'article_id', 'payment_order_id',
                    'amount', 'user_discount', 'article_price', 'article_attributes',)
    fieldsets = (
        ("General info", {'fields': ('article_id', 'payment_order_id',
                                     'number_of_pieces', 'user_discount', 'article_price', 'article_attributes',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('article_id', 'payment_order_id', 'number_of_pieces', 'user_discount', 'article_price', 'article_attributes',),
        }),
    )
    search_fields = ('id', 'article_id__article_name',
                     'payment_order_id__email__email',)
    ordering = ('id', 'article_id__article_name',
                'payment_order_id__email', 'user_discount', 'article_price',)


class PaymentOrderAdmin(admin.ModelAdmin):
    form = PaymentOrderForm
    readonly_fields = ('time_created','time_modified', 'total_cost')
    list_display = ('id', 'full_name', 'address', 'zip_code', 'city', 'phone',
                    'method_of_payment', 'total_cost', 'status', 'time_created')
    list_filter = ('status',)
    fieldsets = (
        ("General info", {'fields': ('email', 'address', 'zip_code',
                                     'city', 'phone', 'method_of_payment', 'status', 'total_cost','time_created','time_modified',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'address', 'zip_code', 'city', 'phone', 'method_of_payment', 'status',),
        }),
    )
    search_fields = ('id', 'email__email', 'address', 'zip_code',
                     'city', 'method_of_payment', 'status',)
    ordering = ('id', 'email__email', 'address', 'zip_code', 'city', 'method_of_payment', 'status', 'total_cost', 'time_created',)

class PaymentOrderCommentHistoryAdmin(admin.ModelAdmin):
    form = PaymentOrderCommentHistoryForm
    readonly_fields = ('time_created', 'status',)
    
    list_display = ('payment_order_id', 'created_by', 'comment', 'status', 'time_created',)
    list_filter = ('status',)

    fieldsets = (
        ("General info", {
            'fields': (
                'payment_order_id', 'comment', 'status', 'time_created',
            )
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'payment_order_id', 'comment',
            ),
        }),
    )
    search_fields = ('payment_order_id', 'status', 'created_by',)
    ordering = ('payment_order_id', 'comment', 'status', 'time_created', 'created_by',)

    def get_form(self, request, *args, **kwargs):
         form = super(PaymentOrderCommentHistoryAdmin, self).get_form(request, *args, **kwargs)
         form.current_user = request.user
         return form


class ArticleGroupAdmin(admin.ModelAdmin):
    form = ArticleGroupForm
    list_display = ('id', 'group_name','show_articles', 'description', 'link')
    fieldsets = (
        ("General info", {
         'fields': ('group_name', 'article_ids', 'description', 'link',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('group_name', 'article_ids', 'description', 'link',),
        }),
    )
    search_fields = ('id', 'group_name', 'article_ids', 'description','link',)
    ordering = ('id', 'group_name', 'article_ids', 'description', 'link',)

    def show_articles(self, obj):
        return " / ".join([a.article_name for a in obj.article_ids.all()])


admin.site.register(Producer, ProducerAdmin)
admin.site.register(ProductGroup, ProductGroupFormAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleImage, ArticleImageAdmin)
admin.site.register(PaymentItem, PaymentItemAdmin)
admin.site.register(PaymentOrder, PaymentOrderAdmin)
admin.site.register(ArticleGroup, ArticleGroupAdmin)
admin.site.register(PaymentOrderCommentHistory, PaymentOrderCommentHistoryAdmin)
