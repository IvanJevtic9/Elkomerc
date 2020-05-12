from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Producer, ProductGroup, Attribute, Article, ArticleImage

class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        fields = [
            'id',
            'producer_name',
            'link',
            'profile_image',
            'description'
        ]

class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = [
            'id',
            'article_id',
            'feature_id',
            'value'
        ]

class ProductGroupForm(forms.ModelForm):
    class Meta:
        model = ProductGroup
        fields = [
            'id',
            'group_name'
        ]

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'id',
            'article_code',
            'article_name',
            'sub_category_id',
            'producer_id',
            'product_group_id',
            'description',
            'price',
            'unit_of_measure',
            'currency',
            'is_available'
        ]

class ArticleImageForm(forms.ModelForm):
    class Meta:
        model = ArticleImage
        fields = [
            'id',
            'article_id',
            'image',
            'image_name',
            'purpose',
            'content_type',
            'size',
            'height',
            'width',
        ]

    def save(self, commit=True):
        article_image = super().save(commit=False)
        if article_image.image_name is None:
            article_image.image_name = self.cleaned_data.get('image').name[0:29] if len(self.cleaned_data.get('image').name) > 30 else self.cleaned_data.get('image').name

        article_image.size = self.cleaned_data.get('image').size
        if hasattr(self.cleaned_data.get('image'), 'content_type'):
            article_image.content_type = self.cleaned_data.get('image').content_type

        if hasattr(self.cleaned_data.get('image'), 'height'):
            article_image.height = self.cleaned_data.get('image').height
        else:
            article_image.height = self.cleaned_data.get('image').image.height   

        if hasattr(self.cleaned_data.get('image'), 'width'):
            article_image.width = self.cleaned_data.get('image').width
        else:
            article_image.width = self.cleaned_data.get('image').image.width

        if commit:
            article_image.save()
        return article_image    