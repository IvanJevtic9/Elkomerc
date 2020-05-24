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

from .serializers import ArticleDetailSerializer, ArticleListSerializer, ProducerSerializer, ProducerListSerializer, ArticleImportSerializer, ArticleImagesImportSerializer, ProducerImagesImportSerializer, PaymentItemDetailSerializer, PaymentItemListSerializer, PaymentOrderListSerializer, PaymentOrderDetailSerializer, PaymentOrderCreateSerializer, PaymentOrderDocumentTransitionSerializer
from product.models import Article, Producer, Attribute, ArticleImage, PaymentItem, PaymentOrder
from account.models import UserDiscount, Account

from account.api.permissions import IsOwner


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


class PaymentItemDetailApiView(mixins.DestroyModelMixin,
                               mixins.UpdateModelMixin,
                               generics.RetrieveAPIView):
    permission_classes = [IsOwner, ]
    serializer_class = PaymentItemDetailSerializer
    pagination_class = None
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        return PaymentItem.objects.all().order_by('id')

    def put(self, request, *args, **kwargs):
        self.check_object_permissions(self.request, self.get_object())
        return self.update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.check_object_permissions(self.request, self.get_object())
        return self.destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request = request.request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = request.user.email
            payment_item_id = int(self.kwargs['id'])

            payment_item = PaymentItem.objects.get(id=payment_item_id)
            article_obj = Article.objects.get(id=payment_item.article_id_id)

            payment_order = PaymentOrder.objects.get(
                id=payment_item.payment_order_id_id)
            item_attributes = serializer.validated_data.get(
                'item_attributes')
            
            payment_order_attributes_notes = ''
            lines = payment_order.attribute_notes.split('\n')
            lines.pop()
            for ln in lines:
                if article_obj.article_name in ln:
                    lines.remove(ln)
                else:
                    payment_order_attributes_notes = payment_order_attributes_notes + ln + '\n'

            payment_order.attribute_notes = payment_order_attributes_notes

            attribute_item = ""
            if item_attributes is not None:
                for att in item_attributes:
                    attribute_item = attribute_item + "Ime artikla: {2},Ime atributa: {0},vrednost atributa: {1}\n".format(
                        att.get('attribute_name'), att.get('value'), article_obj.article_name)


            payment_order.attribute_notes = payment_order.attribute_notes + attribute_item
            payment_order.save()

            user_discount = UserDiscount.objects.filter(email=email)
            user_discount = user_discount.filter(
                product_group_id=article_obj.product_group_id_id)
            if user_discount.exists():
                user_discount = user_discount[0].value
            else:
                user_discount = 0

            payment_item.number_of_pieces = serializer.validated_data.get(
                'number_of_pieces')
            payment_item.article_price = article_obj.price
            payment_item.user_discount = user_discount

            payment_item.save()

            return super().get(request, *args, **kwargs)


class PaymentItemCreateApiView(generics.CreateAPIView,
                               generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = PaymentItemListSerializer

    def get_queryset(self, *args, **kwargs):
        payment_orders = PaymentOrder.objects.filter(
            email=self.request.user.email).order_by('id')
        items = []
        for po in payment_orders:
            qs = PaymentItem.objects.filter(payment_order_id=po)
            for q in qs:
                items.append(q)
        return items

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request = request.request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = request.user.email

            article_id = serializer.validated_data.get('article_id')
            payment_order_id = serializer.validated_data.get(
                'payment_order_id')
            number_of_pieces = serializer.validated_data.get(
                'number_of_pieces')

            payment_order = PaymentOrder.objects.get(id=payment_order_id)
            article_obj = Article.objects.get(id=article_id)
            article_price = article_obj.price

            item_attributes = serializer.validated_data.get(
                'item_attributes')

            attribute_item = ""
            if item_attributes is not None:
                for att in item_attributes:
                    attribute_item = attribute_item + "Ime artikla: {2},Ime atributa: {0},vrednost atributa: {1}\n".format(
                        att.get('attribute_name'), att.get('value'), article_obj.article_name)


            payment_order.attribute_notes = payment_order.attribute_notes + attribute_item
            payment_order.save()

            user_discount = UserDiscount.objects.filter(email=email)
            user_discount = user_discount.filter(
                product_group_id=article_obj.product_group_id)
            if user_discount.exists():
                user_discount = user_discount[0].value
            else:
                user_discount = 0

            payment_item = PaymentItem(article_id=article_obj, payment_order_id=payment_order,
                                       user_discount=user_discount, article_price=article_price, number_of_pieces=number_of_pieces)

            payment_item.save()

            return super().get(request, *args, **kwargs)


class PaymentOrderListApiView(generics.CreateAPIView, generics.ListAPIView):
    permission_classes = [IsOwner, ]
    serializer_class = PaymentOrderListSerializer

    def get_queryset(self, *args, **kwargs):
        #TODO serch for specific payment order
        return PaymentOrder.objects.filter(email=self.request.user.email).order_by('id')

    def post(self, request, *args, **kwargs):
        self.check_object_permissions(self.request, self.get_object())
        return self.create(self, request, *args, **kwargs)


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
            method_of_payment = serializer.validated_data.get(
                'method_of_payment')
            note = serializer.validated_data.get('note')
            email = self.request.user.email
            account_obj = Account.objects.get(email=email)

            address = serializer.validated_data.get('address')
            city = serializer.validated_data.get('city')
            zip_code = serializer.validated_data.get('zip_code')

            payment_order = PaymentOrder(email=account_obj, address=address, city=city,
                                         zip_code=zip_code, method_of_payment=method_of_payment, note=note)
            payment_order.attribute_notes = ""
            payment_order.save()

            items = serializer.validated_data.get('payment_items')
            throw_error = False
            for it in items:
                article_id = it.get('article_id')
                number_of_pieces = it.get('number_of_pieces')

                qs = PaymentItem.objects.filter(article_id=article_id)
                qs = qs.filter(payment_order_id=payment_order.id)
                if qs.exists():
                    throw_error = True

                article = Article.objects.get(id=article_id)
                item_attributes = it.get('item_attributes')
                attribute_item = ""
                if item_attributes is not None:
                    for att in item_attributes:
                        attribute_item = attribute_item + "Ime artikla: {2},Ime atributa: {0},vrednost atributa: {1}\n".format(
                            att.get('attribute_name'), att.get('value'), article.article_name)

                user_discount = UserDiscount.objects.filter(email=email)
                user_discount = user_discount.filter(
                    product_group_id=article.product_group_id)
                if user_discount.exists():
                    user_discount = user_discount[0].value
                else:
                    user_discount = 0

                payment_order.attribute_notes = payment_order.attribute_notes + attribute_item
                payment_order.save()
                payment_item = PaymentItem(article_id=article, payment_order_id=payment_order,
                                           user_discount=user_discount, article_price=article.price, number_of_pieces=number_of_pieces)
                payment_item.save()

            if throw_error:
                payment_order.delete()
                return JsonResponse({"message": "You have multiple payment items for the same article."}, status=400)
            else:
                return JsonResponse({"message": "Payment order has been created."}, status=200)

class PaymentOrderDetailApiView(mixins.DestroyModelMixin,
                               mixins.UpdateModelMixin,
                               generics.RetrieveAPIView):
    permission_classes = [IsOwner, ]
    serializer_class = PaymentOrderDetailSerializer
    pagination_class = None
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        return PaymentOrder.objects.all().order_by('id')

    def put(self, request, *args, **kwargs):
        self.check_object_permissions(self.request, self.get_object())
        return self.update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.check_object_permissions(self.request, self.get_object())
        if serializer.is_valid(raise_exception=True):
            return self.destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request = request.request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            address = serializer.validated_data.get('address')
            zip_code = serializer.validated_data.get('zip_code')
            city = serializer.validated_data.get('city')

            note = serializer.validated_data.get('note')

            payment_order = PaymentOrder.objects.get(id=self.kwargs['id'])
            
            payment_order.address = address
            payment_order.zip_code = zip_code
            payment_order.city = city
            payment_order.note = note
            payment_order.save()

            return super().get(request, *args, **kwargs)

class PaymentOrderDocumentTransitionApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = PaymentOrderDocumentTransitionSerializer

    def get_queryset(self, *args, **kwargs):
        return PaymentOrder.objects.all().order_by('id')

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request = request.request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            payment_order_id = serializer.validated_data.get('payment_order_id')
            transit_status = serializer.validated_data.get('transit_status')
            payment_order = PaymentOrder.objects.get(id=payment_order_id)

            payment_order.status = transit_status
            payment_order.save()

            return JsonResponse({"message": "Payment order status transition has been complited."}, status=200)