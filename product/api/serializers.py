from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from django.utils.translation import ugettext_lazy as _

from product.models import Attribute, Article, ArticleImage, Producer, ProductGroup, PaymentItem, PaymentOrder
from product_category.models import Category, SubCategory

from account.models import Stars, Comments, UserDiscount

import mercantile
import os


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = [
            'id',
            'producer_name',
            'link',
            'profile_image',
            'description'
        ]


class ProducerListSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    sub_categories_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Producer
        fields = [
            'id',
            'producer_name',
            'uri',
            'profile_image',
            'sub_categories_id'
        ]

    def get_sub_categories_id(self, obj):
        sub_categories = []
        artical_list = Article.objects.filter(producer_id=obj.id)

        for art in artical_list:
            sub_categories.append(art.sub_category_id.id)

        return set(sub_categories)

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("product:detail", kwargs={"id": obj.id}, request=request)


class ProducerInfoSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Producer
        fields = [
            'id',
            'producer_name',
            'uri',
            'profile_image'
        ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("product:detail", kwargs={"id": obj.id}, request=request)


class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = [
            'id',
            'group_name'
        ]


class ArticleListSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField(read_only=True)
    uri = serializers.SerializerMethodField(read_only=True)
    article_rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'article_code',
            'article_name',
            'uri',
            'profile_picture',
            'article_rate',
            'price'
        ]

    def get_profile_picture(self, obj):
        profile_image = None
        list_img = ArticleImage.objects.filter(article_id=obj.id)
        host = self.context.get('request')._request._current_scheme_host

        for img in list_img:
            if profile_image is None:
                profile_image = host + img.image.url
            if img.purpose == '#profile_image':
                profile_image = host + img.image.url
                break

        return profile_image

    def get_article_rate(self, obj):
        email = None
        if self.context.get('request').user.id is not None:
            email = self.context.get('request').user.email

        qs = Stars.objects.filter(email=email)
        qs = qs.filter(article_id=obj.id)

        if qs.exists():
            return qs[0].value
        else:
            return None

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("product:article", kwargs={"id": obj.id}, request=request)


class ArticleDetailSerializer(serializers.ModelSerializer):
    producer_info = ProducerInfoSerializer(
        source='producer_id', read_only=True)
    discount_group = ProductGroupSerializer(
        source='product_group_id', read_only=True)
    article_images = serializers.SerializerMethodField(read_only=True)
    currency = serializers.SerializerMethodField(read_only=True)
    attributes = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    unit_of_measure = serializers.SerializerMethodField(read_only=True)
    number_of_rates = serializers.SerializerMethodField(read_only=True)
    avg_rate = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'article_code',
            'article_name',
            'producer_info',
            'category',
            'attributes',
            'article_images',
            'discount_group',
            'description',
            'unit_of_measure',
            'price',
            'currency',
            'number_of_rates',
            'avg_rate',
            'comments',
            'is_available'
        ]

    def get_avg_rate(self, obj):
        rate_sum = 0
        qs = Stars.objects.filter(article_id=obj.id)

        if qs.exists():
            for q in qs:
                rate_sum = rate_sum + q.value

            return rate_sum/len(qs)

        return None

    def get_number_of_rates(self, obj):
        return len(Stars.objects.filter(article_id=obj.id))

    def get_program_info(self, obj):
        request = self.context.get('request')
        program_info = {}
        if(obj.program_id is not None):
            program_info = {
                "program_id": obj.program_id.id,
                "program_name": obj.program_id.program_name,
                "producer_uri": api_reverse("product:detail", kwargs={"id": obj.program_id.producer_id.id}, request=request)
            }

        return program_info

    def get_comments(self, obj):
        comments = []
        qs = Comments.objects.filter(article_id=obj.id)
        for q in qs:
            obj = {
                "comment_id": q.id,
                "email": q.email.email,
                "comment": q.comment,
                "time_created": q.time_created,
                "last_modified": q.last_modified
            }
            comments.append(obj)

        return comments

    def get_article_images(self, obj):
        article_images = []
        list_img = ArticleImage.objects.filter(article_id=obj.id)
        host = self.context.get('request')._request._current_scheme_host

        for img in list_img:
            obj_img = {
                "uri": host+img.image.url,
                "purpose": img.purpose,
                "content_type": img.content_type,
                "height": img.height,
                "width": img.width
            }
            article_images.append(obj_img)

        return article_images

    def get_currency(self, obj):
        return obj.get_currency_display()

    def get_attributes(self, obj):
        attributes = []
        list_att = Attribute.objects.filter(article_id=obj.id)

        for l in list_att:
            obj_att = {
                "attribute_id": l.id,
                "attribute_name": l.feature_id.feature_name,
                "value": l.value,
                "is_selectable": l.feature_id.is_selectable
            }
            attributes.append(obj_att)

        return attributes

    def get_category(self, obj):
        category = {
            "category_id": obj.sub_category_id.category_id.id,
            "category_name": obj.sub_category_id.category_id.category_name,
            "sub_category_id": obj.sub_category_id.id,
            "sub_category_name": obj.sub_category_id.sub_category_name
        }

        return category

    def get_unit_of_measure(self, obj):
        return obj.get_unit_of_measure_display()


class ArticleImportSerializer(serializers.ModelSerializer):
    file_import = serializers.FileField(required=True)

    class Meta:
        model = Article
        fields = [
            'file_import'
        ]

    def validate_file_import(self, value):
        return value


class ArticleImagesImportSerializer(serializers.ModelSerializer):
    directory_path = serializers.CharField(max_length=500, required=True)
    exel_file = serializers.FileField(required=True)

    class Meta:
        model = ArticleImage
        fields = [
            'exel_file',
            'directory_path'
        ]

    def validate_exel_file(self, value):
        return value


class ProducerImagesImportSerializer(serializers.ModelSerializer):
    directory_path = serializers.CharField(max_length=500, required=True)
    exel_file = serializers.FileField(required=True)

    class Meta:
        model = Producer
        fields = [
            'exel_file',
            'directory_path'
        ]

    def validate_exel_file(self, value):
        return value


class PaymentItemDetailSerializer(serializers.ModelSerializer):
    article_code = serializers.SerializerMethodField(read_only=True)
    article_name = serializers.SerializerMethodField(read_only=True)
    unit_of_measure = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PaymentItem
        fields = [
            'id',
            'article_id',
            'payment_order_id',
            'article_code',
            'article_name',
            'number_of_pieces',
            'unit_of_measure',
            'user_discount',
            'article_price',
            'reject_comment',
            'price'
        ]
        read_only_fields = ['payment_order_id',
                            'article_id', 'user_discount', 'article_price', 'reject_comment']

    def get_article_code(self, obj):
        return obj.article_id.article_code

    def get_article_name(self, obj):
        return obj.article_id.article_name

    def get_unit_of_measure(self, obj):
        return obj.article_id.get_unit_of_measure_display()

    def get_price(self, obj):
        return obj.article_price - (obj.user_discount * obj.article_price/100)

    def validate(self, data):
        email = self.context.get('request').user.email
        data = self.context.get('request').data

        payment_order_id = data.get('payment_order_id')
        payment_order = PaymentOrder.objects.get(id=payment_order_id)

        if payment_order.email_id != email:
            raise serializers.ValidationError(
                {'payment_order_id': _("#OWNER_PERMISSION")})

        if payment_order.status in ["RE", "SS", "PD"]:
            raise serializers.ValidationError(
                {'payment_order_id': _("#ORDER_STATUS_ERROR")}) 

class PaymentItemListSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField(read_only=True)
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = PaymentItem
        fields = [
            'uri',
            'article_id',
            'payment_order_id',
            'number_of_pieces',
            'user_discount',
            'article_price',
            'reject_comment',
            'price'
        ]

        read_only_fields = ['article_price', 'user_discount', 'reject_comment']

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("product:item_detail", kwargs={"id": obj.id}, request=request)

    def get_price(self, obj):
        return obj.article_price - (obj.user_discount * obj.article_price/100)

    def validate(self, data):
        email = self.context.get('request').user.email
        data = self.context.get('request').data

        payment_order_id = data.get('payment_order_id')
        article_id = data.get('article_id')
        number_of_pieces = data.get('number_of_pieces')

        if number_of_pieces is None or number_of_pieces is '':
            raise serializers.ValidationError(
                {'number_of_pieces': _("#MUST_BE_GREATER_THEN_ZERO")})

        if int(number_of_pieces) < 1:
            raise serializers.ValidationError(
                {'number_of_pieces': _("#MUST_BE_GREATER_THEN_ZERO")})

        qs = PaymentOrder.objects.filter(id=payment_order_id)
        if not qs.exists():
            raise serializers.ValidationError(
                {'payment_order_id': _("#PAYMENT_ORDER_DOES_NOT_EXIST")})
        else:
            payment_order = qs[0]

        if payment_order.email_id != email:
            raise serializers.ValidationError(
                {'payment_order_id': _("#OWNER_PERMISSION")})

        if payment_order.status in ["RE", "SS", "PD"]:
            raise serializers.ValidationError(
                {'payment_order_id': _("#ORDER_STATUS_ERROR")})

        qs = Article.objects.filter(id=article_id)
        if not qs.exists():
            raise serializers.ValidationError(
                {'article_id': _("#ARTICLE_DOES_NOT_EXIST")})
        else:
            article = qs[0]

        qs = PaymentItem.objects.filter(article_id=article_id)
        qs = qs.filter(payment_order_id=payment_order_id)
        if qs.exists():
            raise serializers.ValidationError(
                {'article_id': _("#ARTICLE_ALREADY_IN_ORDER")})

        payment_order.status = "DR"
        payment_order.save()

        return data

class PaymentOrderListSerializer(serializers.ModelSerializer):
    items = PaymentItemDetailSerializer(read_only=True, many=True)
    class Meta:
        model = PaymentOrder
        fields = [
            'id',
            'email',
            'items',
            'time_created',
            'method_of_payment',
            'status'
        ]
        read_only_fields = ['email','time_created','status']
