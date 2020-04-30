from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from django.utils.translation import ugettext_lazy as _

from product.models import Attribute, Article, ArticleImage, Producer, ProducerImage, Program
from product_category.models import Category, SubCategory

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = [
            'id',
            'program_name'
        ]

class ProducerSerializer(serializers.ModelSerializer):
    producer_images = serializers.SerializerMethodField(read_only=True)
    programs = ProgramSerializer(source='program',read_only=True,many=True)
    class Meta:
        model = Producer
        fields = [
            'id',
            'producer_name',
            'description',
            'programs',
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
    programs = ProgramSerializer(source='program',read_only=True,many=True)
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Producer
        fields = [
            'id',
            'producer_name',
            'uri',
            'programs',
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

class ArticleSerializer(serializers.ModelSerializer):
    program_info = serializers.SerializerMethodField(read_only=True)
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
            'description',
            'program_info',
            'category',
            'attributes',
            'article_images',
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
                "value": l.value
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