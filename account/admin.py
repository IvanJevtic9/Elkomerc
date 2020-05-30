from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Account,
    User,
    Company,
    PostCode,
    Stars,
    WishList,
    Comments,
    UserDiscount)

from .forms import (
    UserForm,
    CompanyForm,
    AccountCreateForm,
    PostForm,
    StarsForm,
    WishListForm,
    CommentsForm,
    UserDiscountForm)


class PostCodeAdmin(ImportExportModelAdmin):
    form = PostForm
    list_display = ('id', 'zip_code', 'city')
    fieldsets = (
        ("General info", {'fields': ('zip_code', 'city')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('zip_code', 'city'),
        }),
    )
    search_fields = ('zip_code', 'city',)
    ordering = ('zip_code', 'city',)


class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ('id', 'first_name', 'last_name', 'email', 'date_of_birth')

    fieldsets = (
        ("General info", {'fields': ('first_name',
                                     'last_name', 'email', 'date_of_birth')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'date_of_birth'),
        }),
    )
    search_fields = ('first_name', 'last_name', 'email__email')
    ordering = ('first_name', 'email',)


class CompanyAdmin(admin.ModelAdmin):
    form = CompanyForm
    list_display = ('id', 'company_name', 'email', 'pib', 'fax')

    fieldsets = (
        ("General info", {'fields': ('company_name', 'email', 'pib', 'fax')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'company_name', 'pib', 'fax'),
        }),
    )
    search_fields = ('company_name', 'email__email', 'pib', 'fax')
    ordering = ('company_name', 'email',)


class AccountAdmin(BaseUserAdmin):
    add_form = AccountCreateForm

    list_display = ('id', 'email', 'address', 'zip_code', 'city',
                    'phone_number', 'account_type', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'account_type')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('address', 'zip_code',
                                      'city', 'phone_number', 'profile_image')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'address', 'zip_code', 'city', 'phone_number'),
        }),
    )
    search_fields = ('email', 'city')
    ordering = ('email',)
    filter_horizontal = ()

class StarsAdmin(admin.ModelAdmin):
    form = StarsForm
    list_display = ('id', 'email', 'article_id', 'value')

    fieldsets = (
        ("General info", {'fields': ('email', 'article_id', 'value',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'article_id', 'value', ),
        }),
    )
    search_fields = ('article_id__article_name', 'email__email', 'value',)
    ordering = ('article_id__article_name', 'email', 'value',)

class WishListAdmin(admin.ModelAdmin):
    form = WishListForm
    list_display = ('id', 'email', 'article_id',)

    fieldsets = (
        ("General info", {'fields': ('email', 'article_id',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'article_id', ),
        }),
    )
    search_fields = ('article_id__article_name', 'email__email',)
    ordering = ('article_id__article_name', 'email',)

class CommentsAdmin(admin.ModelAdmin):
    readonly_fields = ('time_created', 'last_modified')
    form = CommentsForm
    list_display = ('id', 'email', 'article_id', 'comment','time_created', 'last_modified', 'parent_comment_id', 'approved')
    list_filter = ('approved',)

    fieldsets = (
        ("General info", {'fields': ('email', 'article_id', 'comment', 'parent_comment_id', 'approved')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'article_id', 'comment', 'parent_comment_id', 'approved', ),
        }),
    )
    search_fields = ('article_id__article_name', 'email__email', 'comment', 'parent_comment_id__comment','approved')
    ordering = ('article_id__article_name', 'email', 'comment', 'parent_comment_id__comment', 'approved')

class UserDiscountAdmin(admin.ModelAdmin):
    form = UserDiscountForm
    list_display = ('id', 'email', 'product_group_id', 'value')

    fieldsets = (
        ("General info", {'fields': ('email', 'product_group_id', 'value',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'product_group_id', 'value', ),
        }),
    )
    search_fields = ('email__email', 'product_group_id__group_name', 'value',)
    ordering = ('email__email', 'product_group_id__group_name', 'value',)

# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(PostCode, PostCodeAdmin)
admin.site.register(Stars, StarsAdmin)
admin.site.register(WishList, WishListAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(UserDiscount, UserDiscountAdmin)

admin.site.unregister(Group)
