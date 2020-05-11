from rest_framework.response import Response
from rest_framework import generics, mixins, permissions
from rest_framework_jwt.settings import api_settings

from django.db.models import Q
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image

from django.core.files.base import ContentFile
from io import BytesIO
from io import StringIO
import sys

from tablib import Dataset
import openpyxl

from .serializers import ArticleDetailSerializer, ArticleListSerializer, ProducerSerializer, ProducerListSerializer, ArticleImportSerializer, ArticleImagesImportSerializer
from product.models import Article, Producer, Attribute, ArticleImage

from account.api.permissions import AdminAuthenticationPermission

class ArticleListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ArticleListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = Article.objects.all()

        category_id_query = dict(
            self.request.GET.lists()).get('category_id', None)
        sub_category_id_query = dict(
            self.request.GET.lists()).get('sub_category_id', None)
        value_query = dict(self.request.GET.lists()).get('value', None)
        category_name = self.request.GET.get('category_name', None)
        sub_category_name = self.request.GET.get('sub_category_name', None)
        producer_query = self.request.GET.get('producer', None)

        if category_id_query:
            queryset_list = queryset_list.filter(
                Q(sub_category_id__category_id__in=category_id_query)
            ).distinct()
        if sub_category_id_query:
            queryset_list = queryset_list.filter(
                Q(sub_category_id__in=sub_category_id_query)
            ).distinct()
        if category_name:
            queryset_list = queryset_list.filter(
                Q(sub_category_id__category_id__category_name__iexact=category_name)
            ).distinct()
        if sub_category_name:
            queryset_list = queryset_list.filter(
                Q(sub_category_id__sub_category_name__iexact=sub_category_name)
            ).distinct()
        if producer_query:
            queryset_list = queryset_list.filter(
                Q(producer_id=producer_query)
            ).distinct()

        attr_queryset = Attribute.objects.all()
        if value_query:
            attr_queryset = attr_queryset.filter(
                Q(value__in=value_query)
            ).distinct()

            articles_id = []
            for val in attr_queryset:
                articles_id.append(val.id)

            queryset_list = queryset_list.filter(
                Q(id__in=articles_id)
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

            wb = openpyxl.load_workbook(file_import)
            sheet_name = wb.active.title
            excel_sheet = wb.get_sheet_by_name(sheet_name)
            if excel_sheet.max_column is not 6:
                JsonResponse({"message": "Excel file is not valid."}, status=401)

            excel_sheet.insert_rows(0)
            excel_sheet['A1'].value = 'PRODUCT_GROUP'
            excel_sheet['B1'].value = 'ARTICLE_CODE'
            excel_sheet['C1'].value = 'ARTICLE_NAME'
            excel_sheet['D1'].value = 'UNIT_OF_MEASURE'
            excel_sheet['E1'].value = 'BUY_PRICE'
            excel_sheet['F1'].value = 'SELL_PRICE'

            wb.save(file_import)

            dataset = Dataset()
            imported_data = dataset.load(request.FILES[file_import.field_name])
            
            for art in imported_data.dict:
                try:
                    art_obj = Article.objects.get(article_code=art['ARTICLE_CODE'])
                    art_obj.price = art['SELL_PRICE']
                    if art_obj.price == 0:
                        art_obj.is_available = False
                    art_obj.save()
                except Article.DoesNotExist:
                    pass
            
            return JsonResponse({"message": "File has been imported successfully."}, status=200)

class ArticleImagesImportApiView(generics.CreateAPIView):
    permission_classes = [AdminAuthenticationPermission]
    serializer_class = ArticleImagesImportSerializer
    queryset = ArticleImage.objects.all()

    def get_serializer_class(self):
        return ArticleImagesImportSerializer
        
    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request = request.request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            exel_file_import = serializer.validated_data.get('exel_file')
            path = serializer.validated_data.get('directory_path')

            dataset = Dataset()
            imported_data = dataset.load(request.FILES[exel_file_import.field_name])
            
            for art in imported_data.dict:
                #Convert PIL image to django file upload
                image_file = Image.open(path+art['image_name'])
                split_name = image_file.filename.split('\\')
                image_file.filename = split_name[len(split_name)-1]
                
                buffer = BytesIO()
                image_file.save(buffer, format=image_file.format, quality=100)
                buffer.seek(0)
                image_django_file = InMemoryUploadedFile(buffer, image_file.filename, split_name[len(split_name)-1], 'image/jpeg', buffer.tell(), None)
                
                try:
                    article_image = ArticleImage.objects.get(id=art['id'])
                    article_image.image_name = split_name[len(split_name)-1][0:29] if len(split_name[len(split_name)-1]) > 30 else split_name[len(split_name)-1]
                    try:
                        article_obj = Article.objects.get(id=art['article_id'])
                    except Article.DoesNotExist:
                        JsonResponse({"message": "Article with provided id: "+ str(art['article_id']) + "does not exist."}, status=200)

                    article_image.article_id = article_obj
                    article_image.content_type = image_file.format
                    article_image.size = image_file.decodermaxblock
                    article_image.height = image_file.height
                    article_image.width = image_file.width
                    article_image.purpose = art['purpose']

                    article_image.image.delete(save=False)
                    
                    article_image.image.save(image_django_file.name,image_django_file)
                    article_image.save()
                except ArticleImage.DoesNotExist:
                    try:
                        article_obj = Article.objects.get(id=art['article_id'])
                    except Article.DoesNotExist:
                        JsonResponse({"message": "Article with provided id: "+ str(art['article_id']) + "does not exist."}, status=200)

                    image_name = split_name[len(split_name)-1][0:29] if len(split_name[len(split_name)-1]) > 30 else split_name[len(split_name)-1]
                    article_image = ArticleImage(id=art['id'],image=image_django_file,image_name=image_name,article_id=article_obj,content_type=image_file.format,size=image_file.decodermaxblock,height=image_file.height,width=image_file.width,purpose=art['purpose'])

                    article_image.save()

            return JsonResponse({"message": "Images have been imported sucessfully."}, status=200)

class ArticleDetailApiView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ArticleDetailSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        return Article.objects.all()

class ProducerDetailApiView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProducerSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        return Producer.objects.all()


class ProducerListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProducerListSerializer
    pagination_class = None

    def get_queryset(self, *args, **kwargs):
        return Producer.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}
