from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from django.utils.translation import ugettext_lazy as _
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from django.contrib.auth.hashers import check_password

import datetime

from rest_framework_jwt.settings import api_settings
from account.models import Account, Company, User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta = api_settings.JWT_EXPIRATION_DELTA


class AccountRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'email',
            'password',
            'password2',
            'address',
            'city',
            'post_code',
            'phone_number',
            'account_type',
            'token',
            'expires'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        try:
            validators.validate_password(password=value)
        except exceptions.ValidationError as e:
            message = e.messages[0]
            raise serializers.ValidationError(_(message))

        return value

    def validate_password2(self, value):
        request = self.context.get('request')
        pw1 = request.data.get('password')
        pw2 = value

        if pw1 != pw2:
            raise serializers.ValidationError(_("Passwords don't match."))

        return value

    def get_token(self, obj):
        account = obj
        payload = jwt_payload_handler(account)
        token = jwt_encode_handler(payload)

        return token

    def get_expires(self, obj):
        return datetime.datetime.now() + expire_delta

    def validate(self, data):
        # Ovde ide validacija vezana za Company ili User
        data = self.context.get('request').data
        data.pop('password2')
        account_type = data.get('account_type')

        if account_type == "CMP":
            company_name = data.get('company_name', None)
            pib = data.get('pib', None)

            if company_name is None:
                raise serializers.ValidationError({'company_name': _('This company name is required.')})

            if pib is None:
                raise serializers.ValidationError({'pib': _("Pib is required.")})

            qs_company = Company.objects.filter(company_name=company_name)
            if qs_company.exists():
                raise serializers.ValidationError({'company_name': _('This company name already exists.')})
        else:
            first_name = data.get('first_name')
            if first_name is None:
                raise serializers.ValidationError({'first_name': _("Frist name is required.")})

        return data

    def create(self, validated_data):
        address = validated_data.get('address', None)
        city = validated_data.get('city', None)
        post_code = validated_data.get('post_code', None)
        phone_number = validated_data.get('phone_number', None)
        account_type = validated_data.get('account_type', None)

        account_obj = Account(
            email=(validated_data.get('email')), address=address, city=city, post_code=post_code, phone_number=phone_number, account_type=account_type)
        account_obj.set_password(validated_data.get('password'))
        account_obj.is_active = False # TODO Email comfirmation need to be implemented, then is_active - True

        account_obj.save()

        if account_type == "CMP":
            company_name = validated_data.get('company_name')
            pib = validated_data.get('pib')
            fax = validated_data.get('fax')

            company_obj = Company(
                email=account_obj, company_name=company_name, pib=pib, fax=fax)
            company_obj.save()

        else:
            first_name = validated_data.get('first_name')
            last_name = validated_data.get('last_name')
            date_of_birth = validated_data.get('date_of_birth')

            user_obj = User(email=account_obj, first_name=first_name,
                            last_name=last_name, date_of_birth=date_of_birth)
            user_obj.save()

        return account_obj

    def to_representation(self, obj):
        # get the original representation
        ret = super(AccountRegisterSerializer, self).to_representation(obj)

        ret.pop('address')
        ret.pop('post_code')
        ret.pop('city')
        ret.pop('phone_number')
        ret.pop('account_type')
        
        return ret 

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

class AccountListSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True, many=True)
    class Meta: 
        model = Account
        fields = [
            'id',
            'email',
            'address',
            'city',
            'post_code',
            'phone_number',
            'account_type',
            'company',
            'user'
        ]

class AccountDetailSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True, many=True)
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    old_password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    class Meta:
        model = Account
        fields = [
            'id',
            'email',
            'address',
            'city',
            'post_code',
            'phone_number',
            'account_type',
            'company',
            'user',
            'old_password',
            'password',
        ]
    def validate_email(self, value):
        request = self.context.get('request')
        path = request.stream.path
        account_id = int(next(filter(str.isdigit, path.split('/'))))
        
        try:
            acc_obj = Account.objects.get(id=account_id)
        except Account.DoesNotExist:
            raise serializers.ValidationError(_("Email address is not valid."))

        if acc_obj.email != value:
            raise serializers.ValidationError(_("Email address is not valid."))

        return value

    def validate_old_password(self, value):
        request = self.context.get('request')
        email = request.data.get('email')
        old_password = Account.objects.get(email=email).password

        if not check_password(value, old_password):
            raise serializers.ValidationError(_("Invalid password."))

        return value

    def validate_password(self, value):
        try:
            validators.validate_password(password=value)
        except exceptions.ValidationError as e:
            message = e.messages[0]
            raise serializers.ValidationError(_(message))

        return value

    def validate(self, data):
        # Ovde ide validacija vezana za Company ili User
        data = self.context.get('request').data
        account_type = data.get('account_type')
        email = data.get('email')

        if account_type == "CMP":
            company_name = data.get('company_name', None)
            pib = data.get('pib', None)

            if company_name is None:
                raise serializers.ValidationError(
                    {'company_name': _("Company name is required.")})

            if pib is None:
                raise serializers.ValidationError({'pib': _("Pib is required.")})

            qs_company = Company.objects.get(company_name=company_name)
            if qs_company.email != email and  qs_company is not None:
                raise serializers.ValidationError({'company_name': _('This company name already exists.')})
        else:
            first_name = data.get('first_name')
            if first_name is None:
                raise serializers.ValidationError({'first_name': _("Frist name is required.")})

        return data
    
    def create(self, validated_data):
        account_obj = Account.objects.get(email=validated_data.get('email'))
        return account_obj