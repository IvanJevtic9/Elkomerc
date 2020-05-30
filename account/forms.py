from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Account, User, Company, PostCode, Stars, WishList, Comments, UserDiscount

class AccountCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = [
            'email',
            'profile_image',
            'address',
            'zip_code',
            'city',
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

        edit = False if self.instance.id is None else True
        account_changed = False if (not edit) or self.instance.email_id == email else True

        qs_user = User.objects.filter(email=email)
        qs_company = Company.objects.filter(email=email) 
        if (qs_user.exists() or qs_company.exists()) and account_changed:
            raise forms.ValidationError(_('This email address is already used by another user.'))

        if (qs_user.exists() or qs_company.exists()) and not edit:
            raise forms.ValidationError(_('This email address is already used by another user.'))

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
        qs = Account.objects.get(email=email)

        edit = False if self.instance.id is None else True
        account_changed = False if (not edit) or self.instance.email_id == email else True
        company_name_changed = False if (not edit) or self.instance.company_name == company_name else True

        qs_company = Company.objects.filter(company_name=company_name)
        if qs_company.exists() and not edit:
            raise forms.ValidationError(_('This company name already exists.'))
        
        if qs_company.exists() and company_name_changed:
            raise forms.ValidationError(_('This company name already exists.'))

        qs_user = User.objects.filter(email=email)
        qs_company = Company.objects.filter(email=email) 
        if (qs_user.exists() or qs_company.exists()) and account_changed:
            raise forms.ValidationError(_('This email address is already used by another user.'))

        if (qs_user.exists() or qs_company.exists()) and not edit:
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

class StarsForm(forms.ModelForm):
    class Meta:
        model = Stars
        fields = [
            'id',
            'email',
            'article_id',
            'value'
        ]

    def clean(self, *args, **kwargs):
        email = self.data.get('email')
        article_id = int(self.data.get('article_id'))
        value = int(self.data.get('value'))

        edit = False if self.instance.id is None else True
        changed_email = False if (not edit) or self.instance.email_id == email else True
        changed_article = False if (not edit) or self.instance.article_id_id == article_id else True

        qs = Stars.objects.filter(email=email)
        qs = qs.filter(article_id=article_id)
        if qs.exists() and not edit:
            raise forms.ValidationError(_('This user already rate the article.'))

        if (changed_email or changed_article) and qs.exists():
            raise forms.ValidationError(_('This user already rate the article.'))

        if value > 5 or value < 1:
            raise forms.ValidationError(_('Start rate must be between or equal 1 and 5.'))
        
        return super().clean(*args, **kwargs)

class WishListForm(forms.ModelForm):
    class Meta:
        model = WishList
        fields = [
            'id',
            'email',
            'article_id'
        ]

    def clean(self, *args, **kwargs):
        email = self.data.get('email')
        article_id = int(self.data.get('article_id'))

        edit = False if self.instance.id is None else True
        changed_email = False if (not edit) or self.instance.email_id == email else True
        changed_article = False if not edit or self.instance.article_id_id == article_id else True

        qs = WishList.objects.filter(email=email)
        qs = qs.filter(article_id=article_id)
        if qs.exists() and not edit:
            raise forms.ValidationError(_('This user already has the article in the wishlist.'))
        
        if (changed_email or changed_article) and qs.exists():
            raise forms.ValidationError(_('This user already rate the article.'))

        return super().clean(*args, **kwargs)

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = [
            'id',
            'email',
            'article_id',
            'comment',
            'parent_comment_id',
            'approved'
        ]

    def clean(self, *args, **kwargs):
        parent_comment_id = self.data.get('parent_comment_id', None)
        parent_comment = None
        
        if parent_comment_id is not None and parent_comment_id != '':    
            parent_comment = Comments.objects.get(id=parent_comment_id)

        article_id = int(self.data.get('article_id', None))
        if parent_comment is not None and parent_comment.article_id_id != article_id:
            raise forms.ValidationError(_('Article has to be same as parent comment.'))

        return super().clean(*args, **kwargs)

class UserDiscountForm(forms.ModelForm):
    class Meta: 
        model = UserDiscount
        fields = [
            'id',
            'email',
            'product_group_id',
            'value'
        ]