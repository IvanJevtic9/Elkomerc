from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import (
                    Producer, 
                    ProductGroup,
                    Attribute, 
                    Article, 
                    ArticleImage, 
                    PaymentItem, 
                    PaymentOrder, 
                    ArticleGroup, 
                    PaymentOrderCommentHistory)

from account.models import UserDiscount, Account, User, Company


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
            article_image.image_name = self.cleaned_data.get('image').name[0:29] if len(
                self.cleaned_data.get('image').name) > 30 else self.cleaned_data.get('image').name

        article_image.size = self.cleaned_data.get('image').size
        if hasattr(self.cleaned_data.get('image'), 'content_type'):
            article_image.content_type = self.cleaned_data.get(
                'image').content_type

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

class PaymentOrderForm(forms.ModelForm):
    class Meta:
        model = PaymentOrder
        fields = [
            'id',
            'email',
            'full_name',
            'address',
            'city',
            'zip_code',
            'phone',
            'method_of_payment',
            'status',
            'total_cost'
        ]

    def save(self, commit=True):
        payment_order = super().save(commit=False)
        account = Account.objects.get(email=payment_order.email_id)

        if account.account_type is 'USR':
            full_name = User.objects.get(email=account.email).__str__()
        else:
            full_name = Company.objects.get(email=account.email).__str__()

        if payment_order.address == None:
            payment_order.address = account.address
        if payment_order.city == None:
            payment_order.city = account.city
        if payment_order.zip_code == None:
            payment_order.zip_code = account.zip_code
        if payment_order.status == None:
            payment_order.status = "OH"

        payment_order.full_name = full_name

        payment_order.save()

        return payment_order

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

        order_id_changed = False if self.instance.payment_order_id_id == payment_order_id else True
        article_id_changed = False if self.instance.article_id_id == article_id else True

        qs = PaymentItem.objects.filter(payment_order_id=payment_order_id)
        qs = qs.filter(article_id=article_id)

        error = forms.ValidationError(
            _('Article: ' + str(article_id) + ' - this article already exists on the payment order'))
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
        user_discount = UserDiscount.objects.filter(
            product_group_id=article_obj.product_group_id)
        user_discount = user_discount.filter(
            email=payment_item.payment_order_id.email_id)
        if user_discount.exists():
            payment_item.user_discount = user_discount[0].value
        else:
            payment_item.user_discount = 0

        payment_item.save()
        
        payment_order = self.cleaned_data['payment_order_id']
        payment_items = PaymentItem.objects.filter(payment_order_id=payment_order.id)
        
        payment_order.total_cost = 0
        for item in payment_items:
            if item.valid in ['0', '1']:
                payment_order.total_cost += ((item.article_price - (item.user_discount * item.article_price / 100)) * item.number_of_pieces)

        payment_order.save()

        return payment_item

class PaymentOrderCommentHistoryForm(forms.ModelForm):
    class Meta:
        model = PaymentOrderCommentHistory
        fields = [
            'id',
            'payment_order_id',
            'status',
            'created_by',
            'comment'
        ]
    def save(self, commit=True):
        payment_comment = super().save(commit=False)

        payment_comment.created_by = self.current_user
        payment_comment.status = payment_comment.payment_order_id.status
        payment_comment.save()
        
        return payment_comment


class ArticleGroupForm(forms.ModelForm):
    class Meta:
        model = ArticleGroup
        fields = [
            'id',
            'group_name',
            'article_ids',
            'description',
            'link'
        ]
