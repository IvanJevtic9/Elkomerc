from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from django.utils.translation import ugettext_lazy as _

from product_category.models import Category, SubCategory, Feature, FloorFeature
from product.models import Attribute

class SubCategorySerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = SubCategory
        fields = [
            'id',
            'sub_category_name',
            'features'
        ]

    def get_features(self, obj):
        features = []
        id = obj.id

        qs_list = FloorFeature.objects.filter(sub_category_id=id)
        for q in qs_list:
            feat_obj = {
                "id": q.feature_id.id,
                "feature_name": q.feature_id.feature_name,
                "data_type": q.feature_id.data_type,
                "attributes": [],
                "is_selectable": q.feature_id.is_selectable
            }

            att_list = Attribute.objects.filter(feature_id=q.feature_id.id)
            for att in att_list:
                att_obj = {
                    'id': att.id,
                    'value': att.value
                }
                feat_obj.get('attributes').append(att_obj)

            features.append(feat_obj)

        return features


class SubCategoryPublicSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = SubCategory
        fields = [
            'id',
            'category_id',
            'sub_category_name',
            'uri'
        ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("category:detail", kwargs={"id": obj.id}, request=request)

class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategoryPublicSerializer(source='sub_category',read_only=True,many=True)
    class Meta:
        model = Category
        fields = [
            'id',
            'category_name',
            'sub_categories'
        ]