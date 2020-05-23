from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from django.core.validators import validate_email
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

from .managers import CustomUserManager

class PostCode(models.Model):
    zip_code = models.CharField(max_length=15)
    city = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Post code"
        verbose_name_plural = "Post codes"

    def __str__(self):
        return self.city

class Account(AbstractUser):
    ACC_TYPE = (
        ('USR','User'),
        ('CMP','Company')
    )
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_('email address'), validators=[validate_email], unique=True)
    address = models.CharField(max_length=100,blank=True,null=True)
    zip_code = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=17,blank=True,null=True)
    account_type = models.CharField(max_length=3,choices=ACC_TYPE,default='USR')
    profile_image = models.ImageField(blank=True,null=True,upload_to='profile_img/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.email

class User(models.Model):
    email = models.ForeignKey('Account', to_field='email', on_delete=models.CASCADE, related_name='user')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30,blank=True,null=True)                 
    date_of_birth = models.DateField(blank=True,null=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        if self.first_name:
            fullName = self.first_name
        if self.last_name:
            fullName = fullName + ' ' + self.last_name     
        return fullName

class Company(models.Model):
    email = models.ForeignKey('Account', to_field='email', on_delete=models.CASCADE, related_name='company')
    company_name = models.CharField(max_length=50, unique=True)
    pib = models.CharField(max_length=30)                 
    fax = models.CharField(max_length=17, blank=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.company_name

class Stars(models.Model):
    email = models.ForeignKey('Account', to_field='email', on_delete=models.CASCADE, related_name='acc_stars')
    article_id = models.ForeignKey('product.Article', to_field='id', on_delete=models.CASCADE,related_name='art_stars')

    value = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    class Meta:
        verbose_name = "Star"
        verbose_name_plural = "Stars"

    def __str__(self):
        return str(self.value) + ' star'

class WishList(models.Model):
    email = models.ForeignKey('Account', to_field='email', on_delete=models.CASCADE, related_name='acc_wishlist')
    article_id = models.ForeignKey('product.Article', to_field='id', on_delete=models.CASCADE,related_name='art_wishlist')

    class Meta:
        verbose_name = "Wish"
        verbose_name_plural = "WishList"

class Comments(models.Model):
    email = models.ForeignKey('Account', to_field='email', on_delete=models.CASCADE, related_name='acc_comments')
    article_id = models.ForeignKey('product.Article', to_field='id', on_delete=models.CASCADE,related_name='art_comments')
    
    time_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=400)

    parent_comment_id = models.ForeignKey('Comments', to_field='id',on_delete=models.CASCADE, related_name='parent_comment',blank=True,null=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.comment

class UserDiscount(models.Model):
    email = models.ForeignKey('Account',to_field='email',on_delete=models.CASCADE, related_name='acc_discount')
    product_group_id = models.ForeignKey('product.ProductGroup', to_field='id', on_delete=models.CASCADE, related_name='grp_discount')

    value = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        verbose_name = "User discount"
        verbose_name_plural = "User discounts"