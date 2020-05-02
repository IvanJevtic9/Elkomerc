from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from django.core.validators import validate_email
from django.core.validators import RegexValidator

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
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
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
        return self.first_name + ' ' + self.last_name

class Company(models.Model):
    email = models.ForeignKey('Account', to_field='email', on_delete=models.CASCADE, related_name='company')
    company_name = models.CharField(max_length=50, unique=True)
    pib = models.CharField(max_length=30)                 
    fax = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.company_name