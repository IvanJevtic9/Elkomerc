from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from django.utils.translation import ugettext_lazy as _

from django.core import exceptions

# from django.contrib.auth import password_validation as validators # request from client , they want password_validator regex for pass validations.
from django.contrib.auth.hashers import check_password
from .regex_validator import (
    password_validator1,
    password_validator2,
    password_validator3,
    password_validator4
)

from django.core.validators import validate_email

import datetime

from rest_framework_jwt.settings import api_settings
from account.models import (Account,
                            Company,
                            User,
                            PostCode,
                            WishList,
                            Stars,
                            Comments)


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta = api_settings.JWT_EXPIRATION_DELTA


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'company_name',
            'pib',
            'fax'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'date_of_birth'
        ]


class PostCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCode
        fields = [
            'id',
            'zip_code',
            'city'
        ]


class PostCodeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCode
        fields = [
            'zip_code',
            'city'
        ]

    def validate_zip_code(self, value):
        qs = PostCode.objects.filter(zip_code=value)
        if qs.exists():
            raise serializers.ValidationError(
                _("This zip code already exists."))

        return value

    def validate_city(self, value):
        qs = PostCode.objects.filter(city=value)
        if qs.exists():
            raise serializers.ValidationError(_("This city already exists."))

        return value


class AccountRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'}, validators=[password_validator1, password_validator2, password_validator3, password_validator4])

    class Meta:
        model = Account
        fields = [
            'email',
            'password',
            'profile_image',
            'address',
            'city',
            'zip_code',
            'phone_number',
            'account_type',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # Ovde ide validacija vezana za Company ili User
        data = self.context.get('request').data
        account_type = data.get('account_type')
        data_info = data.get('data')

        city = data.get('city')
        zip_code = data.get('zip_code')

        if city is not None:
            try:
                post_obj = PostCode.objects.get(city=city)
                if post_obj.zip_code != zip_code:
                    raise serializers.ValidationError(
                        {'zip_code': _("Provided zip code is invalid.")})
            except PostCode.DoesNotExist:
                pass

        if zip_code is not None:
            try:
                post_obj = PostCode.objects.get(zip_code=zip_code)
                if post_obj.city != city:
                    raise serializers.ValidationError(
                        {'city': _("Provided city is invalid.")})
            except PostCode.DoesNotExist:
                pass

        if account_type == "CMP":
            if data_info is not None:
                company_name = data_info.get('company_name', None)
                pib = data_info.get('pib', None)

            if company_name is None:
                raise serializers.ValidationError(
                    {'company_name': _('This company name is required.')})

            if pib is None:
                raise serializers.ValidationError(
                    {'pib': _("Pib is required.")})

            qs_company = Company.objects.filter(company_name=company_name)
            if qs_company.exists():
                raise serializers.ValidationError(
                    {'company_name': _('This company name already exists.')})
        else:
            if data_info is not None:
                first_name = data_info.get('first_name')
            if first_name is None:
                raise serializers.ValidationError(
                    {'first_name': _("Frist name is required.")})

        return data

    """
    def to_representation(self, obj):
        # get the original representation
        ret = super(AccountRegisterSerializer, self).to_representation(obj)

        ret.pop('address')
        ret.pop('city')
        ret.pop('phone_number')
        ret.pop('account_type')

        return ret
    """


class AccountListSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True, many=True)
    is_active = serializers.BooleanField(read_only=True)
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'id',
            'email',
            'profile_image',
            'uri',
            'city',
            'zip_code',
            'address',
            'phone_number',
            'account_type',
            'company',
            'user',
            'is_active'
        ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("account:detail", kwargs={"id": obj.id}, request=request)


class AccountDetailSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True, many=True)
    email = serializers.EmailField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'id',
            'email',
            'profile_image',
            'address',
            'city',
            'zip_code',
            'phone_number',
            'account_type',
            'company',
            'user',
            'is_active'
        ]

        read_only_fields = ['email']

    def validate(self, data):
        # Ovde ide validacija vezana za Company ili User
        data = self.context.get('request').data
        account_type = data.get('account_type')
        email = self.context.get('request').user.email

        city = data.get('city')
        zip_code = data.get('zip_code')

        if city is not None:
            try:
                post_obj = PostCode.objects.get(city=city)
                if post_obj.zip_code != zip_code:
                    raise serializers.ValidationError(
                        {'zip_code': _("Provided zip code is invalid.")})
            except PostCode.DoesNotExist:
                pass

        if zip_code is not None:
            try:
                post_obj = PostCode.objects.get(zip_code=zip_code)
                if post_obj.city != city:
                    raise serializers.ValidationError(
                        {'city': _("Provided city is invalid.")})
            except PostCode.DoesNotExist:
                pass

        if account_type == "CMP":
            company_name = data.get('company_name', None)
            pib = data.get('pib', None)

            if company_name is None:
                raise serializers.ValidationError(
                    {'company_name': _("Company name is required.")})

            if pib is None:
                raise serializers.ValidationError(
                    {'pib': _("Pib is required.")})

            qs_company = Company.objects.get(company_name=company_name)
            if qs_company.email != email and qs_company is not None:
                raise serializers.ValidationError(
                    {'company_name': _('This company name already exists.')})
        else:
            first_name = data.get('first_name')
            if first_name is None:
                raise serializers.ValidationError(
                    {'first_name': _("Frist name is required.")})

        return data

    def create(self, validated_data):
        email = self.context.get('request').user.email
        account_obj = Account.objects.get(email=email)

        return account_obj


class AccountChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    new_password2 = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'email',
            'old_password',
            'new_password',
            'new_password2'
        ]

    def validate_old_password(self, value):
        request = self.context.get('request')
        path = request.stream.path
        account_id = int(next(filter(str.isdigit, path.split('/'))))

        old_password = Account.objects.get(id=account_id).password

        if value != None and not check_password(value, old_password):
            raise serializers.ValidationError(_("Invalid password."))

        return value

    def validate_new_password(self, value):
        try:
            validators.validate_password(password=value)
        except exceptions.ValidationError as e:
            message = e.messages[0]
            raise serializers.ValidationError(_(message))

        return value

    def validate_new_password2(self, value):
        request = self.context.get('request')
        password = request.data.get('new_password')

        if value != password:
            raise serializers.ValidationError(_("Passwords don't match."))

        return value

    def create(self, validated_data):
        email = self.context.get('request').user.email
        account_obj = Account.objects.get(email=email)

        return account_obj


class AccountResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        write_only=True, validators=[validate_email])

    class Meta:
        model = Account
        fields = [
            'email'
        ]


class WishlistListSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WishList
        fields = [
            'id',
            'email',
            'article_id',
            'uri'
        ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("account:wishlist", kwargs={"id": obj.id}, request=request)   

    def validate(self, obj):
        data = self.context.get('request').data
        email = self.context.get('request').user.email
        article_id = data.get('article_id')

        wish_filter = WishList.objects.filter(email=email)
        wish_filter = wish_filter.filter(article_id=article_id)

        if(wish_filter.exists()):
            raise serializers.ValidationError({'message':_("ALREADY_IN_WISHLIST")})
        
        return data

class WishListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = [
            'id',
            'email',
            'article_id'
        ]

class StarsListSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Stars
        fields = [
            'id',
            'email',
            'article_id',
            'uri',
            'value'
        ]
        read_only_fields = ['email']

    def validate_value(self, value):
        if value > 5 or value < 1:
            raise serializers.ValidationError(_("Invalid rate"))

        return value

    def validate(self, data):        
        data = self.context.get('request').data
        email = self.context.get('request').user.email
        article_id = data.get('article_id')

        star_filter = Stars.objects.filter(email=email)
        star_filter = star_filter.filter(article_id=article_id)

        if(star_filter.exists()):
            raise serializers.ValidationError({'message':_("ALREADY_RATE")})
        
        return data

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("account:stars", kwargs={"id": obj.id}, request=request)      

class StarsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stars
        fields = [
            'id',
            'email',
            'article_id',
            'value'
        ]
        read_only_fields = ['email', 'article_id']

    def validate_value(self, value):
        if value > 5 or value < 1:
            raise serializers.ValidationError(_("RATE_BEETWEEN_1_AND_5"))

        return value

class CommentsListSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Comments
        fields = [
            'id',
            'email',
            'article_id',
            'uri',
            'comment'
        ]
        read_only_fields = ['email']

    def validate_comment(self, value):
        if len(value) > 400 and len(value) < 1:
            raise serializers.ValidationError(_("LENGTH_ERROR"))

        return value

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("account:comments", kwargs={"id": obj.id}, request=request)      

class CommentsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            'id',
            'email',
            'article_id',
            'comment'
        ]
        read_only_fields = ['email', 'article_id']

    def validate_comment(self, value):
        if len(value) > 400 and len(value) < 1:
            raise serializers.ValidationError(_("LENGTH_ERROR"))

        return value