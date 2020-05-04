from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from django.utils.translation import ugettext_lazy as _

from product.models import Attribute, Article, ArticleImage, Producer, ProducerImage, ProductGroup
from product_category.models import Category, SubCategory

class ProducerSerializer(serializers.ModelSerializer):
    producer_images = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Producer
        fields = [
            'id',
            'producer_name',
            'link',
            'description',
            'producer_images'
        ]

    def get_producer_images(self, obj):
        producer_images = []
        list_img = ProducerImage.objects.filter(producer_id=obj.id)
        host = self.context.get('request')._request._current_scheme_host

        for img in list_img:
            obj_img = {
                "uri": host+img.image.url,
                "purpose": img.purpose,
                "content_type": img.content_type,
                "height": img.height,
                "width": img.width
            }
            producer_images.append(obj_img)

        return producer_images

class ProducerListSerializer(serializers.ModelSerializer):
    producer_images = serializers.SerializerMethodField(read_only=True)
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Producer
        fields = [
            'id',
            'producer_name',
            'uri',
            'producer_images'
        ]

    def get_producer_images(self, obj):
        producer_images = []
        list_img = ProducerImage.objects.filter(producer_id=obj.id)
        host = self.context.get('request')._request._current_scheme_host

        for img in list_img:
            obj_img = {
                "uri": host+img.image.url,
                "purpose": img.purpose
            }
            producer_images.append(obj_img)

        return producer_images

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("product:detail", kwargs={"id": obj.id}, request=request)

class ProducerInfoSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField(read_only=True)
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model =  Producer
        fields = [
            'id',
            'producer_name',
            'uri',
            'profile_image'
        ]
    
    def get_profile_image(self, obj):
        profile_image = None
        list_img = ProducerImage.objects.filter(producer_id=obj.id)
        host = self.context.get('request')._request._current_scheme_host

        for img in list_img: 
            if img.purpose == '#profile_icon':
                profile_image = host + img.image.url
                break;

        return profile_image

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

class ArticleSerializer(serializers.ModelSerializer):
    producer_info = ProducerInfoSerializer(source='producer_id',read_only=True)
    discount_group = ProductGroupSerializer(source='product_group',read_only=True)
    article_images = serializers.SerializerMethodField(read_only=True)
    currency = serializers.SerializerMethodField(read_only=True)
    attributes = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    unit_of_measure = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Article
        fields = [
            'id',
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
            'is_available'
        ]

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
                "is_selectable": l.is_selectable
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