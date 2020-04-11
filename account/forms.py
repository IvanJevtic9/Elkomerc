from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Account, User, Company, PostCode

class AccountCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = [
            'email',
            'profile_image',
            'address',
            'post_code_id',
            'phone_number'
        ]

    def clean_password2(self):
        pw1 = self.cleaned_data.get("password1")
        pw2 = self.cleaned_data.get("password2")

        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError(_("Passwords don't match."))
        
        return pw2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'date_of_birth'
        ]

    def clean(self, *args, **kwargs):
        email = self.data.get('email')

        qs = Account.objects.get(email=email)
        if qs is None:
            raise forms.ValidationError(_('Email does not exist.'))
        else:
            qs_user = User.objects.filter(email=email)
            qs_company = Company.objects.filter(email=email) 
            if qs_user.exists() or qs_company.exists():
                raise forms.ValidationError(_('This email address is already used by another user'))

        qs.account_type = 'USR'
        qs.save()

        return super().clean(*args, **kwargs)        

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'email',
            'company_name',
            'pib',
            'fax'
        ]

    def clean(self, *args, **kwargs):
        email = self.data.get('email')

        company_name = self.data.get('company_name')
        qs_company = Company.objects.filter(company_name=company_name)
        if qs_company.exists():
            raise forms.ValidationError(_('This company name already exists.'))

        qs = Account.objects.get(email=email)
        if qs is None:
            raise forms.ValidationError(_('Email does not exist.'))
        else:
            qs_user = User.objects.filter(email=email)
            qs_company = Company.objects.filter(email=email) 
            if qs_user.exists() or qs_company.exists():
                raise forms.ValidationError(_('This email address is already used by another user.'))

        qs.account_type = 'CMP'
        qs.save()

        return super().clean(*args, **kwargs) 

class PostForm(forms.ModelForm):
    class Meta:
        model = PostCode
        fields = [
            'id',
            'zip_code',
            'city'
        ]        