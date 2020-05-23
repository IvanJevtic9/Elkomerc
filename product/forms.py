from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Producer, ProductGroup, Attribute, Article, ArticleImage, PaymentItem, PaymentOrder

from account.models import UserDiscount, Account

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
        
class PaymentItemForm(forms.ModelForm):
    class Meta:
        model = PaymentItem
        fields = [
            'id',
            'article_id',
            'payment_order_id',
            'user_discount',
            'article_price',
            'number_of_pieces'
        ]
    def clean(self, *args, **kwargs):
        id = self.instance.id

        payment_order_id = int(self.data.get('payment_order_id'))
        article_id = int(self.data.get('article_id'))

        order_id_changed = False if self.instance.payment_order_id.id == payment_order_id else True
        article_id_changed = False if self.instance.article_id.id == article_id else True

        qs = PaymentItem.objects.filter(payment_order_id=payment_order_id)
        qs = qs.filter(article_id=article_id)

        error = forms.ValidationError(_('Article: ' + str(article_id) + ' - this article already exists on the payment order'))
        if qs.exists() and id is None:
            raise error
        elif order_id_changed and qs.exists():
            raise error
        elif article_id_changed and qs.exists():
            raise error

        return super().clean(*args, **kwargs)

    def save(self, commit=True):
        payment_item = super().save(commit=False)

        article_obj = Article.objects.get(id=payment_item.article_id_id)
        payment_item.article_price = article_obj.price
        user_discount = UserDiscount.objects.filter(product_group_id=article_obj.product_group_id)
        user_discount = user_discount.filter(email=payment_item.payment_order_id.email_id)
        if user_discount.exists():
            payment_item.user_discount = user_discount[0].value
        else:
            payment_item.user_discount = 0

        payment_item.save()
        return payment_item


class PaymentOrderForm(forms.ModelForm):
    class Meta:
        model = PaymentOrder
        fields = [
            'id',
            'email',
            'method_of_payment',
            'status',
            'note',
            'attribute_notes'
        ]