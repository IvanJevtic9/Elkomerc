from rest_framework.response import Response
from rest_framework import generics, mixins, permissions

from account.api.permissions import IsAdminOrReadOnly

from rest_framework_jwt.settings import api_settings
from .utils import get_article_group_json_obj

from django.db.models import Q
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image

from django.core.files.base import ContentFile
from io import BytesIO
from io import StringIO
import sys
import datetime
import pytz

from tablib import Dataset
import openpyxl

from .serializers import ArticleDetailSerializer, ArticleListSerializer, ProducerSerializer, ProducerListSerializer, ArticleImportSerializer, ArticleImagesImportSerializer, ProducerImagesImportSerializer, ArticleGroupListSerializer, ArticleGroupDetailSerializer, PaymentOrderCreateSerializer, PaymentOrderSerializer, PaymentOrderListSerializer, PaymentOrderUpdateSerializer
from product.models import Article, Producer, Attribute, ArticleImage, PaymentItem, PaymentOrder, ArticleGroup, PaymentOrderCommentHistory
from account.models import UserDiscount, Account, User, Company

from account.api.permissions import IsOwner, IsOwnerOrAdmin

class ArticleListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
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

        attr_queryset = Attribute.objects.all()
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

        if value_query:
            attr_queryset = attr_queryset.filter(
                Q(value__in=value_query)
            ).distinct()

            articles_id = []
            for val in attr_queryset:
                articles_id.append(val.article_id_id)

            queryset_list = queryset_list.filter(
                Q(id__in=articles_id)
            ).distinct()

        return queryset_list


class ArticleImportApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser, ]
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
                JsonResponse(
                    {"message": "Excel file is not valid."}, status=401)

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
                    art_obj = Article.objects.get(
                        article_code=art['ARTICLE_CODE'])
                    art_obj.price = art['SELL_PRICE']
                    if art_obj.price == 0:
                        art_obj.is_available = False
                    art_obj.save()
                except Article.DoesNotExist:
                    pass

            return JsonResponse({"message": "File has been imported successfully."}, status=200)


class ProducerImagesImportApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser, ]
    serializer_class = ProducerImagesImportSerializer
    queryset = Producer.objects.all()

    def get_serializer_class(self):
        return ProducerImagesImportSerializer

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request = request.request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            exel_file_import = serializer.validated_data.get('exel_file')
            path = serializer.validated_data.get('directory_path')

            dataset = Dataset()
            imported_data = dataset.load(
                request.FILES[exel_file_import.field_name])
            for prod in imported_data.dict:
                image_file = Image.open(path+prod['image_name'])
                split_name = image_file.filename.split('\\')

                if image_file.height > 250 and image_file.width > 250 and image_file.mode != 'P':
                    h_p = 200/image_file.height
                    w_p = 200/image_file.width

                    per = h_p if h_p > w_p else w_p

                    image_file = image_file.resize(
                        (int(per*image_file.height), int(per*image_file.width)), Image.ANTIALIAS)

                if image_file.format is None:
                    image_format = split_name[len(split_name)-1].split('.')[1]
                    image_file.format = 'PNG' if image_format == 'png' else 'JPEG'

                image_file.filename = split_name[len(split_name)-1]

                buffer = BytesIO()
                image_file.save(buffer, format=image_file.format, quality=100)
                buffer.seek(0)
                image_django_file = InMemoryUploadedFile(buffer, image_file.filename, split_name[len(
                    split_name)-1], 'image/jpeg', buffer.tell(), None)

                try:
                    producer_obj = Producer.objects.get(id=prod['producer_id'])
                    producer_obj.profile_image.delete(save=False)

                    producer_obj.profile_image.save(
                        image_django_file.name, image_django_file)
                    producer_obj.save()
                except Producer.DoesNotExist:
                    pass
            return JsonResponse({"message": "Images have been imported sucessfully."}, status=200)


class ArticleImagesImportApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser, ]
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
            imported_data = dataset.load(
                request.FILES[exel_file_import.field_name])

            for art in imported_data.dict:
                # Convert PIL image to django file upload
                image_file = Image.open(path+art['image_name'])
                split_name = image_file.filename.split('\\')
                image_file.filename = split_name[len(split_name)-1]

                buffer = BytesIO()
                image_file.save(buffer, format=image_file.format, quality=100)
                buffer.seek(0)
                image_django_file = InMemoryUploadedFile(buffer, image_file.filename, split_name[len(
                    split_name)-1], 'image/jpeg', buffer.tell(), None)

                try:
                    article_image = ArticleImage.objects.get(id=art['id'])
                    article_image.image_name = split_name[len(split_name)-1][0:29] if len(
                        split_name[len(split_name)-1]) > 30 else split_name[len(split_name)-1]
                    try:
                        article_obj = Article.objects.get(id=art['article_id'])
                    except Article.DoesNotExist:
                        JsonResponse({"message": "Article with provided id: " +
                                      str(art['article_id']) + "does not exist."}, status=200)

                    article_image.article_id = article_obj
                    article_image.content_type = image_file.format
                    article_image.size = image_file.decodermaxblock
                    article_image.height = image_file.height
                    article_image.width = image_file.width
                    article_image.purpose = art['purpose']

                    article_image.image.delete(save=False)

                    article_image.image.save(
                        image_django_file.name, image_django_file)
                    article_image.save()
                except ArticleImage.DoesNotExist:
                    try:
                        article_obj = Article.objects.get(id=art['article_id'])
                    except Article.DoesNotExist:
                        JsonResponse({"message": "Article with provided id: " +
                                      str(art['article_id']) + "does not exist."}, status=200)

                    image_name = split_name[len(split_name)-1][0:29] if len(
                        split_name[len(split_name)-1]) > 30 else split_name[len(split_name)-1]
                    article_image = ArticleImage(id=art['id'], image=image_django_file, image_name=image_name, article_id=article_obj, content_type=image_file.format,
                                                 size=image_file.decodermaxblock, height=image_file.height, width=image_file.width, purpose=art['purpose'])

                    article_image.save()

            return JsonResponse({"message": "Images have been imported sucessfully."}, status=200)


class ArticleDetailApiView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ArticleDetailSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        return Article.objects.all()


class ProducerDetailApiView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ProducerSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        return Producer.objects.all()


class ProducerListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = ProducerListSerializer
    pagination_class = None

    def get_queryset(self, *args, **kwargs):
        return Producer.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}



class ArticleGroupListApiView(generics.CreateAPIView,generics.ListAPIView):
    permission_classes = [IsAdminOrReadOnly, ]
    serializer_class = ArticleGroupListSerializer
    pagination_class = None

    def get_queryset(self, *args, **kwargs):
        return ArticleGroup.objects.all().order_by('id')

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request = request.request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            group_name = serializer.validated_data.get('group_name', None)
            article_ids = serializer.validated_data.get('article_ids', None)
            description = serializer.validated_data.get('description', None)
            link = serializer.validated_data.get('link', None)

            art_grp = ArticleGroup(group_name=group_name,description=description,link=link)
            art_grp.save()


            for art_id in article_ids:
                art = Article.objects.get(id=art_id.id)
                art_grp.article_ids.add(art)

            art_grp.save()

            return get_article_group_json_obj(art_grp, request)

class ArticleGroupDetailApiView(mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.RetrieveAPIView):
    permission_classes = [permissions.IsAdminUser, ]
    serializer_class = ArticleGroupDetailSerializer
    pagination_class = None
    lookup_field = 'id'
    
    def get_queryset(self, *args, **kwargs):
        return ArticleGroup.objects.all().order_by('id')

    def delete(self, request, *args, **kwargs):
        self.check_object_permissions(self.request, self.get_object())
        return self.destroy(request, *args, **kwargs)    

    def put(self, request, *args, **kwargs):
        self.check_object_permissions(self.request, self.get_object())
        return self.update(self, request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        request = request.request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=False):
            art_group_id = int(self.kwargs['id'])
            art_group_obj = ArticleGroup.objects.get(id=art_group_id)

            group_name = serializer.validated_data.get('group_name', None)
            article_ids = serializer.validated_data.get('article_ids', None)
            description = serializer.validated_data.get('description', None)
            link = serializer.validated_data.get('link', None)

            if group_name:
                art_group_obj.group_name = group_name
            if description:
                art_group_obj.description = description
            if link:
                art_group_obj.link = link
            if article_ids:
                art_group_obj.article_ids.clear()
                
                for art_id in article_ids:
                    art = Article.objects.get(id=art_id.id)
                    art_group_obj.article_ids.add(art)

            art_group_obj.save()

            return get_article_group_json_obj(art_group_obj, request)

class PaymentOrderCreateApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = PaymentOrderCreateSerializer

    def get_queryset(self, *args, **kwargs):
        return PaymentOrder.objects.all()
    
    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request = request.request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = request.user            

            address = serializer.validated_data.get('method_of_payment', None)
            city = serializer.validated_data.get('city', None)
            zip_code = serializer.validated_data.get('zip_code', None)
            phone = serializer.validated_data.get('phone', None)
            method_of_payment = serializer.validated_data.get('method_of_payment', 'PS')
            comment = serializer.validated_data.get('comment', None)

            account = Account.objects.get(email=user.email)

            full_name = None
            if account.account_type == 'USR':
                full_name = User.objects.get(email=user.email).__str__()
            else:   
                full_name = Company.objects.get(email=user.email).__str__()

            payment_order = PaymentOrder(
                email = account,
                full_name = full_name,
                method_of_payment = method_of_payment,
                status = 'OH',
                address = address,
                city = city,
                zip_code = zip_code,
                phone = phone 
            )
            
            payment_order.save()

            PaymentOrderCommentHistory(
                created_by = account,
                status='OH',
                payment_order_id=payment_order,
                comment=comment
            ).save()

            payment_items = serializer.validated_data.get('payment_items', None)
            for item in payment_items:
                article = item['article_id']
                number_of_pieces = item['number_of_pieces']
                article_attributes = item['article_attributes']

                try:
                    user_discount = UserDiscount.objects.get(email=account.email,product_group_id=article.product_group_id_id).value
                except UserDiscount.DoesNotExist:
                    user_discount = 0

                payment_item = PaymentItem(
                    article_id=article,
                    payment_order_id=payment_order,
                    user_discount=user_discount,
                    number_of_pieces=number_of_pieces,
                    article_price=article.price,
                    article_attributes=article_attributes,
                    valid='1'
                )
                payment_item.save()

                payment_order.total_cost += ((article.price - (user_discount * article.price / 100)) * number_of_pieces)

            payment_order.save()

            return JsonResponse({"message": "Payment order has been created."}, status=200)

class PaymentOrderDetailApiView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrAdmin,]
    serializer_class = PaymentOrderSerializer
    pagination_class = None
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        return PaymentOrder.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request and self.request.method == 'GET':
            return PaymentOrderSerializer
        return PaymentOrderUpdateSerializer

    def get(self, request, *args, **kwargs):
        self.serializer_class = self.get_serializer_class(self,*args, **kwargs)
        return super().get(self, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.serializer_class = self.get_serializer_class(self, *args, **kwargs)
        self.check_object_permissions(self.request, self.get_object())
        return self.update(self, request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        request = request.request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = request.user            

            payment_order = PaymentOrder.objects.get(id=int(self.kwargs['id']))
            account = Account.objects.get(email=user.email)

            address = serializer.validated_data.get('address', None)
            city = serializer.validated_data.get('city', None)
            zip_code = serializer.validated_data.get('zip_code', None)
            phone = serializer.validated_data.get('phone', None)
            status = serializer.validated_data.get('status',None)
            comment = serializer.validated_data.get('comment', '')

            if address:
                payment_order.address = address
            if city:
                payment_order.city = city
            if zip_code:
                payment_order.zip_code = zip_code
            if phone:
                payment_order.phone = phone

            payment_order.status = status

            PaymentOrderCommentHistory(
                created_by = account,
                status=status,
                payment_order_id=payment_order,
                comment=comment
            ).save()

            payment_items = serializer.validated_data.get('payment_items', None)

            existing_payment_items = PaymentItem.objects.filter(payment_order_id=payment_order.id)
            for ei in existing_payment_items:
                if ei.valid == '-1':
                    ei.delete()
                elif ei.valid == '1':
                    ei.valid='0'
                    ei.save()

            if payment_items:
                for item in payment_items:
                    article = item['article_id']
                    number_of_pieces = item['number_of_pieces']
                    article_attributes = item.get('article_attributes',None)

                    try:
                        old_item = existing_payment_items.get(article_id=item['article_id'])
                        old_item.valid = '-1'
                        old_item.save()
                    except PaymentItem.DoesNotExist:
                        pass

                    try:
                        user_discount = UserDiscount.objects.get(email=account.email,product_group_id=article.product_group_id_id).value
                    except UserDiscount.DoesNotExist:
                        user_discount = 0

                    if number_of_pieces is not -1:
                        payment_item = PaymentItem(
                            article_id=article,
                            payment_order_id=payment_order,
                            user_discount=user_discount,
                            number_of_pieces=number_of_pieces,
                            article_price=article.price,
                            article_attributes=article_attributes,
                            valid='1'
                        )
                        payment_item.save()

            new_payment_items = PaymentItem.objects.filter(payment_order_id=payment_order.id)

            payment_order.total_cost = 0
            for item in new_payment_items:
                if item.valid in ['0', '1']:
                    payment_order.total_cost += ((item.article_price - (item.user_discount * item.article_price / 100)) * item.number_of_pieces)

            payment_order.save()                        

            return JsonResponse({"message": "Payment order has been updated."}, status=200) 

class PaymentOrderListApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = PaymentOrderListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = PaymentOrder.objects.all()
        order_field = self.request.GET.get('order_by',None)

        status_query = dict(self.request.GET.lists()).get('status', None)
        full_name_query = self.request.GET.get('full_name', None)
        date_from = self.request.GET.get('date_from',None)
        date_to = self.request.GET.get('date_to',None)

        try:
            if date_from:
                datetime.datetime.strptime(date_from, '%Y-%m-%d')
            else:
                date_from = datetime.datetime(1,1,1,0,0,0,0,tzinfo=pytz.UTC)
            if date_to:
                datetime.datetime.strptime(date_to, '%Y-%m-%d')
            else:
                date_to = datetime.datetime(9999,12,31,0,0,0,0,tzinfo=pytz.UTC)

            if date_from or date_to:
                queryset_list = queryset_list.filter(time_created__range=[date_from,date_to])    
        except ValueError:
            pass

        if status_query:
            queryset_list = queryset_list.filter(
                Q(status__in=status_query)
            ).distinct()

        if full_name_query:
            queryset_list = queryset_list.filter(
                Q(full_name__contains=full_name_query)
            ).distinct()

        if order_field in ['id', 'full_name', 'email', 'status', 'time_created', 'time_modified', 'total_cost', '-id', '-email', '-full_name', '-status', '-time_created', '-time_modified', '-total_cost']:
            queryset_list = queryset_list.order_by(order_field)

        return queryset_list
