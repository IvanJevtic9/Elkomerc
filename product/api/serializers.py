from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from django.utils.translation import ugettext_lazy as _

from product.models import Attribute, Article, ArticleImage, Producer, ProductGroup, PaymentItem, PaymentOrder, ArticleGroup, PaymentOrderCommentHistory
from product_category.models import Category, SubCategory

from account.models import Stars, Comments, UserDiscount, User, Company, Account

from .utils import get_article_detail

import mercantile
import os
import math
import decimal

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
            'producer_name',
            'uri',
            'profile_image'
        ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("product:detail", kwargs={"id": obj.id}, request=request)


class ArticleListSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField(read_only=True)
    uri = serializers.SerializerMethodField(read_only=True)
    article_rate = serializers.SerializerMethodField(read_only=True)
    user_discount = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    avg_rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'article_code',
            'article_name',
            'uri',
            'profile_picture',
            'article_rate',
            'avg_rate',
            'user_discount',
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

    def get_avg_rate(self, obj):
        rate_sum = 0
        qs = Stars.objects.filter(article_id=obj.id)

        if qs.exists():
            for q in qs:
                rate_sum = rate_sum + q.value

            return rate_sum/len(qs)

        return None

    def get_user_discount(self, obj):
        if self.context.get('request').user.is_anonymous:
            return 0
        email = self.context.get('request').user.email
        
        qs = UserDiscount.objects.filter(email=email)
        qs = qs.filter(product_group_id=obj.product_group_id_id)
        if qs.exists():
            return qs[0].value
        return 0

    def get_price(self, obj):
        return int(obj.price)

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
    user_discount = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    user_price = serializers.SerializerMethodField(read_only=True)
    article_images = serializers.SerializerMethodField(read_only=True)
    attributes = serializers.SerializerMethodField(read_only=True)
    unit_of_measure = serializers.SerializerMethodField(read_only=True)
    number_of_rates = serializers.SerializerMethodField(read_only=True)
    avg_rate = serializers.SerializerMethodField(read_only=True)
    article_rate = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'article_code',
            'article_name',
            'producer_info',
            'attributes',
            'article_images',
            'description',
            'unit_of_measure',
            'user_discount',
            'price',
            'user_price',
            'number_of_rates',
            'avg_rate',
            'article_rate',
            'comments',
            'is_available'
        ]

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

    def get_avg_rate(self, obj):
        rate_sum = 0
        qs = Stars.objects.filter(article_id=obj.id)

        if qs.exists():
            for q in qs:
                rate_sum = rate_sum + q.value

            return rate_sum/len(qs)

        return None

    def get_price(self, obj):
        return int(obj.price)

    def get_number_of_rates(self, obj):
        return len(Stars.objects.filter(article_id=obj.id))

    def get_comments(self, obj):
        comments = []
        qs = Comments.objects.filter(article_id=obj.id).order_by('parent_comment_id')
        qs = qs.filter(approved=True)
        for q in qs:
            qs = User.objects.filter(email=q.email_id)
            if qs.exists():
                user = qs[0].__str__()
            else:
                cmp_obj = Company.objects.get(email=q.email_id)
                user = cmp_obj.__str__()

            acc_obj = Account.objects.get(email=q.email_id)
            host = self.context.get('request')._request._current_scheme_host
            if not acc_obj.profile_image:
                profile_image = None
            else:
                profile_image = host + acc_obj.profile_image.url

            obj = {
                'comment_id': q.id,
                'user': user,
                'profile_image': profile_image,
                'comment': q.comment,
                'last_modified': q.last_modified,
                'responses': []
            }
            if q.parent_comment_id_id is None:
                comments.append(obj)
            else:
                index = [i for i,x in enumerate(comments)if q.parent_comment_id_id == x.get('comment_id')]
                if len(index) != 0:
                    index = index[0]
                    obj.pop('responses')
                    comments[index].get('responses').append(obj)

        return comments

    def get_article_images(self, obj):
        article_images = []
        list_img = ArticleImage.objects.filter(article_id=obj.id)
        host = self.context.get('request')._request._current_scheme_host

        for img in list_img:
            obj_img = {
                "uri": host+img.image.url,
                "purpose": img.purpose
            }
            article_images.append(obj_img)

        return article_images

    def get_attributes(self, obj):
        attributes = []
        list_att = Attribute.objects.filter(article_id=obj.id)

        for l in list_att:
            obj_att = {
                "attribute_name": l.feature_id.feature_name,
                "value": l.value,
                "is_selectable": l.feature_id.is_selectable
            }
            attributes.append(obj_att)

        return attributes

    def get_user_discount(self, obj):
        if self.context.get('request').user.is_anonymous:
            return 0
        email = self.context.get('request').user.email

        qs = UserDiscount.objects.filter(email=email)
        qs = qs.filter(product_group_id=obj.product_group_id_id)
        if qs.exists():
            return qs[0].value
        return 0

    def get_user_price(self, obj):
        if self.context.get('request').user.is_anonymous:
            return obj.price
        email = self.context.get('request').user.email
        
        qs = UserDiscount.objects.filter(email=email)
        qs = qs.filter(product_group_id=obj.product_group_id_id)
        if qs.exists():
            value = qs[0].value
        else:
            value = 0
        return obj.price - (obj.price*value/100)

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

class ArticleGroupListSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField(read_only=True)
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ArticleGroup
        fields = [
            'id',
            'group_name',
            'article_ids',
            'articles',
            'description',
            'uri',
            'link'
        ]
        extra_kwargs = {'article_ids': {'write_only': True}}

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("product:article_group", kwargs={"id": obj.id}, request=request)

    def get_articles(self, obj):
        articles = []
        request = self.context.get('request')

        return get_article_detail(obj, request)

class ArticleGroupDetailSerializer(serializers.ModelSerializer): 
    articles = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ArticleGroup
        fields = [
            'id',
            'group_name',
            'article_ids',
            'articles',
            'description',
            'link'
        ]
        extra_kwargs = {'article_ids': {'write_only': True}}

    def get_articles(self, obj):
        articles = []
        request = self.context.get('request')

        return get_article_detail(obj, request)

class PaymentItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentItem
        fields = [
            'article_id',
            'number_of_pieces',
            'article_attributes'
        ]

class PaymentOrderCreateSerializer(serializers.ModelSerializer):
    payment_items = PaymentItemCreateSerializer(many=True)
    comment = serializers.CharField(max_length=300)
    class Meta:
        model = PaymentOrder
        fields = [
            'method_of_payment',
            'address',
            'city',
            'zip_code',
            'phone',
            'comment',
            'payment_items'
        ]

    def validate(self, data):
        if(len(data['payment_items']) < 1):
            raise serializers.ValidationError(
                        {'payment_items': _("There must be at least one payment item.")})
        return data

class PaymentOrderSerializer(serializers.ModelSerializer):
    payment_items = serializers.SerializerMethodField(read_only=True)
    history = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = PaymentOrder
        fields = [
            'id',
            'email',
            'full_name',
            'method_of_payment',
            'status',
            'address',
            'city',
            'zip_code',
            'phone',
            'total_cost',
            'payment_items',
            'time_created',
            'time_modified',
            'history'
        ]
    
    def get_payment_items(self, obj):
        payment_items = PaymentItem.objects.filter(payment_order_id=obj.id)
        items = []

        for item in payment_items:
            items.append({
                'article_id': item.article_id.id,
                'article_code': item.article_id.article_code,
                'name': item.article_id.article_name,
                'count': item.number_of_pieces,
                'unit_of_measure': item.article_id.unit_of_measure,
                'discount': item.user_discount,
                'price': item.article_price,
                'valid': item.valid
            })

        return sorted(items, key= lambda x: int(x['valid']))
    
    def get_history(self, obj):
        comment_history = PaymentOrderCommentHistory.objects.filter(payment_order_id=obj.id)
        history = []

        for comment in comment_history:
            history.append({
                'created_by': comment.created_by.email,
                'comment': comment.comment,
                'status': comment.status,
                'time_created': comment.time_created
            })
        return sorted(history, key= lambda x: x['time_created'])

class PaymentOrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOrder
        fields = [
            'id',
            'full_name',
            'email',
            'status',
            'time_created',
            'time_modified',
            'total_cost'
        ]

class PaymentOrderUpdateSerializer(serializers.ModelSerializer):
    payment_items = PaymentItemCreateSerializer(many=True, required=False)
    comment = serializers.CharField(max_length=300, required=False, allow_blank=True)
    class Meta:
        model = PaymentOrder
        fields = [
            'address',
            'city',
            'zip_code',
            'phone',
            'status',
            'comment',
            'payment_items'
        ]
        extra_kwargs = {'address': {'required': False},'city': {'required': False},'zip_code': {'required': False},'phone': {'required': False}}

    def validate(self, data):
        if data.get('status', None) is None:
            raise serializers.ValidationError({'status': _("Status is required field.")})
        
        if data.get('status', None) not in ['OH', 'IP', 'RJ', 'MF', 'AP', 'SS', 'PR', 'PD']:
            raise serializers.ValidationError({'status': _("Unknown status.")})

        return data