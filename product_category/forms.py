from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Category, SubCategory, Feature, FloorFeature

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'id',
            'category_name'
        ]

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = [
            'id',
            'category_id',
            'sub_category_name'
        ]

class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = [
            'id',
            'feature_name',
            'data_type',
            'is_selectable'
        ]

class FloorFeatureForm(forms.ModelForm):
    class Meta:
        model = FloorFeature
        fields = [
            'id',
            'sub_category_id',
            'feature_id'
        ]