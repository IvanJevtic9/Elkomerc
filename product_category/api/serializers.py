from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from django.utils.translation import ugettext_lazy as _

from product_category.models import Category, SubCategory, Feature, FloorFeature

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = [
            'id',
            'data_type',
            'feature_name'
        ]

class SubCategorySerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = SubCategory
        fields = [
            'id',
            'category_name',
            'sub_category_name',
            'features'
        ]

    def get_category_name(self, obj):
        category = Category.objects.get(id=obj.category_id_id)

        return category.category_name

    def get_features(self, obj):
        features = []
        id = obj.id

        qs_list = FloorFeature.objects.filter(sub_category_id=id)
        for q in qs_list:

            object = {
                "id": q.feature_id.id,
                "feature_name": q.feature_id.feature_name,
                "data_type": q.feature_id.data_type
            }

            features.append(object)

        return features


class SubCategoryPublicSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = SubCategory
        fields = [
            'id',
            'category_id',
            'sub_category_name',
            'features'
        ]

    def get_features(self, obj):
        features = []
        id = obj.id

        qs_list = FloorFeature.objects.filter(sub_category_id=id)
        for q in qs_list:

            object = {
                "id": q.feature_id.id,
                "feature_name": q.feature_id.feature_name,
                "data_type": q.feature_id.data_type
            }

            features.append(object)

        return features


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategoryPublicSerializer(source='sub_category',read_only=True,many=True)
    class Meta:
        model = Category
        fields = [
            'id',
            'category_name',
            'sub_categories'
        ]