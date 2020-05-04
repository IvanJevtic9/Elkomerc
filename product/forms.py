from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Producer, ProducerImage, ProductGroup, Attribute, Article, ArticleImage

class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        fields = [
            'id',
            'producer_name',
            'link',
            'description'
        ]

class ProducerImageForm(forms.ModelForm):
    class Meta:
        model = ProducerImage
        fields = [
            'id',
            'producer_id',
            'image',
            'image_name',
            'purpose',
            'content_type',
            'size',
            'height',
            'width'
        ]

    def save(self, commit=True):
        prod_image = super().save(commit=False)
        if prod_image.image_name is None:
            prod_image.image_name = self.cleaned_data.get('image').name[0:29] if len(self.cleaned_data.get('image').name) > 30 else self.cleaned_data.get('image').name

        prod_image.size = self.cleaned_data.get('image').size
        if hasattr(self.cleaned_data.get('image'), 'content_type'):
            prod_image.content_type = self.cleaned_data.get('image').content_type
        if hasattr(self.cleaned_data.get('image'), 'height'):
            prod_image.height = self.cleaned_data.get('image').height
        else:
            prod_image.height = self.cleaned_data.get('image').image.height   

        if hasattr(self.cleaned_data.get('image'), 'width'):
            prod_image.width = self.cleaned_data.get('image').width
        else:
            prod_image.width = self.cleaned_data.get('image').image.width

        if commit:
            prod_image.save()
        return prod_image

class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = [
            'id',
            'article_id',
            'feature_id',
            'value',
            'is_selectable'
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
            'article_name',
            'sub_category_id',
            'producer_id',
            'product_group',
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