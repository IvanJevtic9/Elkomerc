from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions
from rest_framework_jwt.settings import api_settings

from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from django.template.loader import render_to_string
import json

from account.activation_tokens import account_activation_token, account_change_password_token
from .serializers import AccountRegisterSerializer, AccountListSerializer, AccountDetailSerializer, AccountChangePasswordSerializer, PostCodeSerializer, PostCodeCreateSerializer, AccountResetPasswordSerializer
from account.models import Account, Company, User, PostCode

from .permissions import AnonPermissionOnly, IsOwnerOrReadOnly

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class AuthView(APIView):
    authentication_classes = []
    permission_classes = [AnonPermissionOnly, ]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'message': 'You are already authenticated'}, status=400)
        data = request.data
        email = data.get('email')
        password = data.get('password')
        account = authenticate(email=email, password=password)
        
        no_email = False
        no_active = False

        qs = Account.objects.filter(email__iexact=email)
        if(qs.count() == 0):
            no_email = True 
        else:
            qs = qs.filter(is_active=True)
            if qs.count() == 0:
                no_active = True
        
        if qs.count() == 1:
            account_obj = qs.first()
            if account_obj.check_password(password):
                account = account_obj
                payload = jwt_payload_handler(account)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, email)

                return Response(response)
            else:
                return Response({"message": "INVALID_PASSWORD"}, status=401)
        else:
            if no_email:
                return Response({"message": "EMAIL_NOT_EXSIST"}, status=404)
            if no_active:
                return Response({"message": "USER_NOT_ACTIVE"}, status=404)


class RegisterAPIView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountRegisterSerializer
    permission_classes = [AnonPermissionOnly, ]
    # TODO Customize register view template ,currently its not possible to create this via rest-api post method

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_serializer_class(self):
        return AccountRegisterSerializer

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request = request.request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            address = serializer.validated_data.get('address', None)

            city = serializer.validated_data.get('city', None)
            zip_code = serializer.validated_data.get('zip_code', None)

            phone_number = serializer.validated_data.get('phone_number', None)
            account_type = serializer.validated_data.get('account_type', None)
            image = serializer.validated_data.get('profile_image', None)

            if city is not None:
                try:
                    post_code_obj = PostCode.objects.get(city=city)
                except PostCode.DoesNotExist:
                    post_code_obj = None
            else:
                try:
                    post_code_obj = PostCode.objects.get(zip_code=zip_code)
                except PostCode.DoesNotExist:
                    post_code_obj = None

            account_obj = Account(
                email=(serializer.validated_data.get('email')), address=address, post_code_id=post_code_obj, phone_number=phone_number, account_type=account_type)
            account_obj.set_password(serializer.validated_data.get('password'))
            account_obj.profile_image = image
            account_obj.is_active = False

            account_obj.save()

            if account_type == "CMP":
                company_name = serializer.validated_data.get('company_name')
                pib = serializer.validated_data.get('pib')
                fax = serializer.validated_data.get('fax')

                company_obj = Company(
                    email=account_obj, company_name=company_name, pib=pib, fax=fax)
                company_obj.save()

            else:
                first_name = serializer.validated_data.get('first_name')
                last_name = serializer.validated_data.get('last_name')
                date_of_birth = serializer.validated_data.get('date_of_birth')

                user_obj = User(email=account_obj, first_name=first_name,
                                last_name=last_name, date_of_birth=date_of_birth)
                user_obj.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'account': account_obj,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(account_obj.id)),
                'token': account_activation_token.make_token(account_obj),
            })

            to_email = serializer.validated_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            return JsonResponse({"message": "Please confirm your email address to complete the registration."}, status=200)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        account_obj = Account.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        account_obj = None
    if account_obj is not None and account_activation_token.check_token(account_obj, token):
        account_obj.is_active = True
        account_obj.save()
        # return redirect('home')
        return JsonResponse({"message": "Thank you for your email confirmation. Now you can login on your account."}, status=200)
    else:
        return JsonResponse({"message": "Activation link is invalid!"}, status=500)


class ChangePasswordViaEmailAPIView(generics.CreateAPIView):
    serializer_class = AccountResetPasswordSerializer
    permission_classes = [AnonPermissionOnly, ]

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

    def get_serializer_class(self):
        return AccountResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        request = request.request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            to_email = serializer.validated_data.get('email')
            account_obj = Account.objects.get(email=to_email)

            current_site = get_current_site(request)
            mail_subject = 'Change password.'
            message = render_to_string('acc_change_password.html', {
                'account': account_obj,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(account_obj.id)),
                'token': account_change_password_token.make_token(account_obj),
            })

            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

        return JsonResponse({"message": "Please check your email address to reset password."}, status=200)

def reset_password(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        account_obj = Account.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        account_obj = None
    if account_obj is not None and account_change_password_token.check_token(account_obj, token):
        
        # return redirect('home')
        return JsonResponse({"message": "Reset password"}, status=200)
    else:
        return JsonResponse({"message": "Activation link is invalid!"}, status=500)

class AccountListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = AccountListSerializer

    def get_queryset(self, *args, **kwargs):
        email_query = self.request.GET.get('email')
        city_query = self.request.GET.get('city')
        company_name = self.request.GET.get('company_name')
        first_name = self.request.GET.get('first_name')
        queryset_list = Account.objects.filter(is_active=True)

        if email_query or city_query or company_name or first_name:
            queryset_list = queryset_list.filter(
                Q(email__icontains=email_query)
            ).distinct()
        if city_query:
            queryset_list = queryset_list.filter(
                Q(city__icontains=city_query)
            ).distinct()
        if company_name:
            queryset_list = queryset_list.filter(
                Q(company__company_name__icontains=company_name)
            ).distinct()
        if first_name:
            queryset_list = queryset_list.filter(
                Q(user__first_name__icontains=first_name)
            ).distinct()

        return queryset_list

    def get_serializer_context(self):
        return {'request': self.request}


class AccountDetailApiView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.RetrieveAPIView
):
    permission_classes = [IsOwnerOrReadOnly, ]
    serializer_class = AccountDetailSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        return Account.objects.all()

    def get_serializer_class(self):
        return AccountDetailSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.save()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            account_id = self.kwargs['id']
            account = Account.objects.get(id=account_id)

            # account info
            address = serializer.validated_data.get('address', None)
            city = serializer.validated_data.get('city', None)
            zip_code = serializer.validated_data.get('zip_code', None)
            phone_number = serializer.validated_data.get('phone_number', None)
            account_type = serializer.validated_data.get('account_type')
            image = serializer.validated_data.get('profile_image', None)

            if city is not None:
                post_code_obj = PostCode.objects.get(city=city)
            else:
                post_code_obj = PostCode.objects.get(zip_code=zip_code)
            # user info - if exist
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            date_of_birth = serializer.validated_data.get('date_of_birth')
            # company info - if exist
            company_name = serializer.validated_data.get('company_name')
            pib = serializer.validated_data.get('pib')
            fax = serializer.validated_data.get('fax')

            if account_type != account.account_type:
                if account.account_type == "USR":
                    User.objects.filter(email=account.email).delete()
                    company_obj = Company(
                        email=account, company_name=company_name, pib=pib, fax=fax)
                    company_obj.save()
                else:
                    Company.objects.filter(email=account.email).delete()
                    user_obj = User(email=account, first_name=first_name,
                                    last_name=last_name, date_of_birth=date_of_birth)
                    user_obj.save()
            else:
                if account.account_type == "USR":
                    user_obj = User.objects.get(email=account.email)
                    user_obj.first_name = first_name
                    user_obj.last_name = last_name
                    user_obj.date_of_birth = date_of_birth
                    user_obj.save()
                else:
                    company_obj = Company.objects.get(email=account.email)
                    company_obj.company_name = company_name
                    company_obj.pib = pib
                    company_obj.fax = fax
                    company_obj.save()

            account.address = address
            account.post_code_id = post_code_obj
            account.phone_number = phone_number
            account.account_type = account_type
            if account.profile_image is None:
                account.profile_image = image
            else:
                account.profile_image.delete(save=False)
                account.profile_image = image

            account.save()

        return JsonResponse({"message": "Account has been updated successfully."}, status=200)


class AccountChangePassword(
    mixins.UpdateModelMixin,
    generics.RetrieveAPIView
):
    permission_classes = [IsOwnerOrReadOnly, ]
    serializer_class = AccountChangePasswordSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        return Account.objects.all()

    def get_serializer_class(self):
        return AccountChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.save()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            account_id = self.kwargs['id']
            account_obj = Account.objects.get(id=account_id)

            password = serializer.validated_data.get('new_password', None)
            account_obj.set_password(password)
            account_obj.save()

            return JsonResponse({"message": "Password has been changed successfully."}, status=200)


class PostCodeListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostCodeSerializer

    def get_queryset(self, *args, **kwargs):
        zip_code_query = self.request.GET.get('zip_code')
        city_query = self.request.GET.get('city')

        queryset_list = PostCode.objects.all()
        if zip_code_query:
            queryset_list = queryset_list.filter(
                Q(zip_code__icontains=zip_code_query)
            ).distinct()
        if city_query:
            queryset_list = queryset_list.filter(
                Q(city__icontains=city_query)
            ).distinct()

        return queryset_list


class PostCodeDetailView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = PostCodeCreateSerializer
    queryset = PostCode.objects.all()

    def get_serializer_class(self):
        return PostCodeCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request = request.request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            zip_code = serializer.validated_data.get('zip_code', None)
            city = serializer.validated_data.get('city', None)

            post_code_obj = PostCode(zip_code=zip_code, city=city)
            post_code_obj.save()

            return Response({"message": "Post code has been created."}, status=201)
