from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from site_configurations.models import Corosel

class CoroselListSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Corosel
        fields = [
            'id',
            'name',
            'description',
            'link',
            'corosel_image',
            'is_enabled',
            'uri'
        ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("site_configurations:detail", kwargs={"id": obj.id}, request=request)


class CoroselDetailSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Corosel
        fields = [
            'id',
            'name',
            'description',
            'link',
            'is_enabled',
            'corosel_image'
        ]

