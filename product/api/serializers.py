from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from django.utils.translation import ugettext_lazy as _

from product.models import Attribute, Article, ArticleImage, Producer, ProductGroup, PaymentItem, PaymentOrder
from product_category.models import Category, SubCategory

from account.models import Stars, Comments, UserDiscount, User, Company, Account

import mercantile
import os
import math


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

    class Meta:
        model = Article
        fields = [
            'id',
            'article_code',
            'article_name',
            'uri',
            'profile_picture',
            'article_rate',
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

    def get_user_discount(self, obj):
        if self.context.get('request').user.is_anonymous:
            return 0
        email = self.context.get('request').user.email
        qs = UserDiscount.objects.filter(email=email)

        if qs.exists():
            return qs.filter(product_group_id=obj.product_group_id_id)[0].value
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
            'article_rate',
            'comments',
            'is_available'
        ]

    def get_article_rate(self, obj):
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
        return qs.filter(product_group_id=obj.product_group_id_id)[0].value

    def get_user_price(self, obj):
        if self.context.get('request').user.is_anonymous:
            return obj.price
        email = self.context.get('request').user.email
        qs = UserDiscount.objects.filter(email=email)
        value = qs.filter(product_group_id=obj.product_group_id_id)[0].value

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


class PaymentItemDetailSerializer(serializers.ModelSerializer):
    article_code = serializers.SerializerMethodField(read_only=True)
    article_name = serializers.SerializerMethodField(read_only=True)
    unit_of_measure = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    article_price = serializers.SerializerMethodField(read_only=True)

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

    def get_article_price(self, obj):
        return int(obj.article_price)

    def validate(self, data):
        email = self.context.get('request').user.email
        data = self.context.get('request').data

        id = int(self.context.get(
            'request').parser_context.get('kwargs').get('id'))
        payment_item = PaymentItem.objects.get(id=id)
        payment_order_id = payment_item.payment_order_id
        payment_order = PaymentOrder.objects.get(id=payment_order_id.id)

        if payment_order.email_id != email:
            raise serializers.ValidationError(
                {'payment_order_id': _("#OWNER_PERMISSION")})

        if payment_order.status in ["RE", "SS", "PD"]:
            raise serializers.ValidationError(
                {'payment_order_id': _("#ORDER_STATUS_ERROR")})

        return data


class PaymentItemListSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField(read_only=True)
    uri = serializers.SerializerMethodField(read_only=True)
    article_price = serializers.SerializerMethodField(read_only=True)

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

        read_only_fields = ['user_discount', 'reject_comment']

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("product:item_detail", kwargs={"id": obj.id}, request=request)

    def get_price(self, obj):
        return obj.article_price - (obj.user_discount * obj.article_price/100)

    def get_article_price(self, obj):
        return int(obj.article_price)

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
    total_cost = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = PaymentOrder
        fields = [
            'id',
            'email',
            'address',
            'zip_code',
            'city',
            'items',
            'time_created',
            'method_of_payment',
            'note',
            'attribute_notes',
            'total_cost',
            'status'
        ]
        read_only_fields = ['email', 'time_created', 'status', 'attribute_notes']

    def get_total_cost(self, obj):
        items = PaymentItem.objects.filter(payment_order_id=obj.id)
        total_sum = 0

        for item in items:
            total_sum = total_sum + \
                (item.article_price - (item.user_discount *
                                       item.article_price/100)) * item.number_of_pieces

        return math.ceil(total_sum)

    def get_status(self, obj):
        return obj.get_status_display()

class PaymentOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOrder
        fields = [
            'id',
            'email',
            'address',
            'zip_code',
            'city',
            'time_created',
            'method_of_payment',
            'note',
            'attribute_notes',
            'status'
        ]

        read_only_fields = ['email', 'time_created', 'status', 'attribute_notes']    

    def validate(self, data):
        data = self.context.get('request').data

        items = data.get('payment_items')
        for it in items:
            article_id = it.get('article_id')
            number_of_pieces = it.get('number_of_pieces')

            if number_of_pieces is None or number_of_pieces is '':
                raise serializers.ValidationError(
                    {'number_of_pieces': _("#MUST_BE_GREATER_THEN_ZERO")})

            if int(number_of_pieces) < 1:
                raise serializers.ValidationError(
                    {'number_of_pieces': _("#MUST_BE_GREATER_THEN_ZERO")})

            qs = Article.objects.filter(id=article_id)
            if not qs.exists():
                raise serializers.ValidationError(
                    {'article_id': _("Article with id {0} doesn't exist".format(article_id))})

        return data


class PaymentOrderDetailSerializer(serializers.ModelSerializer):
    items = PaymentItemDetailSerializer(read_only=True, many=True)
    total_cost = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = PaymentOrder
        fields = [
            'id',
            'email',
            'address',
            'zip_code',
            'city',
            'items',
            'time_created',
            'method_of_payment',
            'note',
            'attribute_notes',
            'total_cost',
            'status'
        ]

        read_only_fields = ['email', 'time_created', 'status', 'attribute_notes'] 

    def get_total_cost(self, obj):
        items = PaymentItem.objects.filter(payment_order_id=obj.id)
        total_sum = 0

        for item in items:
            total_sum = total_sum + \
                (item.article_price - (item.user_discount *
                                       item.article_price/100)) * item.number_of_pieces

        return math.ceil(total_sum)

    def get_status(self, obj):
        return obj.get_status_display()

    def validate(self, data):
        id = self.context.get('request').parser_context.get('kwargs').get('id')
        payment_order = PaymentOrder.objects.get(id=id)
        if payment_order.status in ["RE", "SS", "PD"]:
            raise serializers.ValidationError(
                    {'status': _("#PAYMENT_ORDER_IN_NOT_VALID_STATUS_FOR_UPDATE")})

        return data

class PaymentOrderDocumentTransitionSerializer(serializers.ModelSerializer):
    payment_order_id = serializers.IntegerField(required=True)
    transit_status = serializers.CharField(max_length=2, required=True)
    class Meta:
        model = PaymentOrder
        fields = [
            'payment_order_id',
            'transit_status'
        ]
    
    def validate_payment_order_id(self,value):
        try:
            payment_order = PaymentOrder.objects.get(id=value)
        except PaymentOrder.DoesNotExist:
            raise serializers.ValidationError(_('#PAYMENT_ORDER_DOES_NOT_EXIST'))    
        
        return value

    def validate(self, data):
        email = self.context.get('request').user.email
        is_superuser = self.context.get('request').user.is_superuser

        transit_status = data.get('transit_status')

        payment_order = PaymentOrder.objects.get(id=data.get('payment_order_id'))
        status = payment_order.status

        if payment_order.email_id != email and not is_superuser:
            raise serializers.ValidationError({"user":_('#DO_NOT_HAVE_PERMISSION')})   
    
        if (status == "DR" and transit_status == "IN") or \
           (status == "RW" and transit_status == "DR" ):
            return data    
        elif ((status == "IN" and transit_status == "RE" ) or \
           (status == "IN" and transit_status == "RW" ) or \
           (status == "IN" and transit_status == "WF" ) or \
           (status == "WF" and transit_status == "SS" ) or \
           (status == "SS" and transit_status == "PD" )) and \
            is_superuser:
            return data
        else:
            raise serializers.ValidationError({"transition":_('#NOT_ALLOWED_TRANSITION')}) 

        return data