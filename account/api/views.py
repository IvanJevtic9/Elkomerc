from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions
from rest_framework_jwt.settings import api_settings

from django.db.models import Q
from django.contrib.auth import authenticate
from django.http import JsonResponse
import json

from .serializers import AccountRegisterSerializer, AccountListSerializer, AccountDetailSerializer
from account.models import Account, Company, User

from .permissions import AnonPermissionOnly, IsOwnerOrReadOnly

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

class AuthView(APIView):
    authentication_classes = []
    permission_classes = [AnonPermissionOnly, ]
    
    def post(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'detail': 'You are already authenticated'}, status=400)
        data = request.data
        email = data.get('email')
        password = data.get('password')
        account = authenticate(email=email, password=password)

        qs = Account.objects.filter(email__iexact=email)

        if qs.count() == 1:
            account_obj = qs.first()
            if account_obj.check_password(password):
                account = account_obj
                payload = jwt_payload_handler(account)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, email)

                return Response(response)
        return Response({"detail": "Invalid credentials."},status=401)

class RegisterAPIView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountRegisterSerializer 
    permission_classes = [permissions.IsAuthenticated, ]
    # TODO Customize register view template ,currently its not possible to create this via rest-api post method     

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}           

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
        return Account.object.all()

    def get_serializer_class(self):
        return AccountDetailSerializer 

    def put (self, request, *args, **kwargs):
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
            password = serializer.validated_data.get('password')
            address = serializer.validated_data.get('address', None)
            city = serializer.validated_data.get('city', None)
            post_code = serializer.validated_data.get('post_code', None)
            phone_number = serializer.validated_data.get('phone_number', None)
            account_type = serializer.validated_data.get('account_type')
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
                    company_obj = Company(email=account,company_name=company_name,pib=pib,fax=fax)
                    company_obj.save()
                else:
                    Company.objects.filter(email=account.email).delete()
                    user_obj = User(email=account,first_name=first_name,last_name=last_name,date_of_birth=date_of_birth)
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

            account.set_password(password)
            account.address = address
            account.city = city
            account.post_code = post_code
            account.phone_number = phone_number
            account.account_type = account_type
            account.save()

        return JsonResponse({"message": "Account has been updated successfully."},status=200)       

    
