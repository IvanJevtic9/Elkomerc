from rest_framework.response import Response
from rest_framework import generics, mixins, permissions
from rest_framework_jwt.settings import api_settings

from django.db.models import Q
from django.contrib.auth import authenticate
from django.http import JsonResponse

from tablib import Dataset
import pandas as pa

from .serializers import ArticleSerializer, ProducerSerializer, ProducerListSerializer , ArticleImportSerializer
from product.models import Article, Producer
from product.resources import ArticleResource

from account.api.permissions import AdminAuthenticationPermission

class ArticleListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ArticleSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = Article.objects.all()

        category_id_query = self.request.GET.get('category_id',None)
        sub_category_id_query = self.request.GET.get('sub_category_id',None)  
        category_name = self.request.GET.get('category_name',None)
        sub_category_name = self.request.GET.get('sub_category_name',None)

        if category_id_query:
            queryset_list = queryset_list.filter(
                Q(sub_category_id__category_id=category_id_query)                
            ).distinct()
        if sub_category_id_query:
            queryset_list = queryset_list.filter(
                Q(sub_category_id=sub_category_id_query)                
            ).distinct()
        if category_name:
            queryset_list = queryset_list.filter(
                Q(sub_category_id__category_id__category_name__iexact=category_name)                
            ).distinct()
        if sub_category_name:
            queryset_list = queryset_list.filter(
                Q(sub_category_id__sub_category_name__iexact=sub_category_name)                
            ).distinct()            

        return queryset_list

class ArticleImportApiView(generics.CreateAPIView):
    permission_classes = [AdminAuthenticationPermission]
    serializer_class = ArticleImportSerializer
    queryset = Article.objects.all()

    def get_serializer_class(self):
        return ArticleImportSerializer

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request = request.request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            file_import = serializer.validated_data.get('file_import')

            dataset = Dataset()
            imported_data = dataset.load(request.FILES[file_import.field_name])

            for art in imported_data.dict:
                try:
                    art_obj = Article.objects.get(id=art['SIFRA'])
                    art_obj.price = art['PROD.CEN']
                    art_obj.save()
                except Article.DoesNotExist:
                    pass

            return JsonResponse({"message": "File has been imported successfully."}, status=200)

class ProducerDetailApiView(generics.RetrieveAPIView): 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProducerSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        return Producer.objects.all()

class ProducerListApiView(generics.ListAPIView): 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProducerListSerializer

    def get_queryset(self, *args, **kwargs):
        return Producer.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}     