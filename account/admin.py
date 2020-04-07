from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Account, User, Company

from .forms import (UserForm,
                    CompanyForm,
                    AccountCreateForm)

class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ('id', 'first_name', 'last_name', 'email', 'date_of_birth')

    fieldsets = (
        ("General info", {'fields': ('first_name', 'last_name', 'email', 'date_of_birth')}),
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

    list_display = ('id', 'email', 'address', 'city', 'post_code', 'phone_number', 'account_type', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'account_type')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('address', 'city', 'post_code', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'address', 'city', 'post_code', 'phone_number'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Company, CompanyAdmin)

admin.site.unregister(Group)