from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

# Create your models here.
class Producer(models.Model):
    producer_name = models.CharField(max_length=30, unique=True)
    link = models.TextField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(
        upload_to='producer_img/', blank=True, null=True)
    description = models.TextField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Producer"
        verbose_name_plural = "Producers"

    def __str__(self):
        return self.producer_name


class Attribute(models.Model):
    article_id = models.ForeignKey(
        'Article', to_field='id', on_delete=models.CASCADE, related_name='attribute_article')
    feature_id = models.ForeignKey('product_category.Feature', to_field='id',
                                   on_delete=models.CASCADE, related_name='attribute_feature')
    value = models.TextField(max_length=30)

    class Meta:
        verbose_name = "Attribute"
        verbose_name_plural = "Attributes"

    def __str__(self):
        return self.feature_id.feature_name


class ProductGroup(models.Model):
    group_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Product group"
        verbose_name_plural = "Product groups"

    def __str__(self):
        return self.group_name

class Article(models.Model):
    CURRENCY_TYPE = (
        ('RSD', 'Dinar'),
        ('EUR', 'Euro')
    )
    MEASURE_TYPE = (
        ("M", "Metar"),
        ("K", "Kilogram"),
        ("P", "Komada")
    )

    article_code = models.CharField(max_length=15, unique=True)
    article_name = models.CharField(max_length=80)
    sub_category_id = models.ForeignKey(
        'product_category.SubCategory', to_field='id', on_delete=models.CASCADE, related_name='article')
    producer_id = models.ForeignKey('Producer', to_field='id', on_delete=models.CASCADE,
                                    blank=True, null=True, related_name='article_producer')
    product_group_id = models.ForeignKey(
        'ProductGroup', to_field='id', on_delete=models.CASCADE, related_name='article_group')

    price = models.DecimalField(max_digits=20, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.01'))])
    currency = models.CharField(
        max_length=3, choices=CURRENCY_TYPE, default='RSD')
    unit_of_measure = models.CharField(
        max_length=1, choices=MEASURE_TYPE, default="P")
    description = models.TextField(max_length=200, blank=True, null=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.article_name


class ArticleImage(models.Model):
    article_id = models.ForeignKey(
        'Article', to_field='id', on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to='article_img/')
    image_name = models.CharField(max_length=30, blank=True, null=True)
    content_type = models.CharField(max_length=20, blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    purpose = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Article image"
        verbose_name_plural = "Article images"

    def __str__(self):
        return self.image_name

class ArticleGroup(models.Model):
    group_name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    link = models.CharField(max_length=100,blank=True,null=True)
    article_ids = models.ManyToManyField(Article)

    class Meta:
        verbose_name = "Article group"
        verbose_name_plural = "Article groups"

    def __str__(self):
        return self.group_name    

#Payment order status types
STATUS_TYPE = (
        ("OH", "NA_CEKANJU"),
        ("IP", "U_OBRADI"),
        ("RJ", "ODBIJENO"),
        ("MF", "MODIFIKOVANO"),
        ("AP", "ODOBRENO_ZA_SLANJE"),
        ("SS", "POSLATO"),
        ("PR", "VRACENA"),
        ("PD", "ISPORUCENJA"),
    )

METHOD_OF_PAYMENT_TYPE = (
    ("PS", "KUCNA_DOSTAVA"),
)

#Only None and true payment items are valid on soem payment order.
VALID_TYPE = (
    ("-1", "FALSE"),
    ("0", "NONE"),
    ("1", "TRUE"),
)

class PaymentOrder(models.Model):
    email = models.ForeignKey('account.Account', to_field='email', on_delete=models.CASCADE, related_name='order_email')
    full_name = models.CharField(max_length=61)
    
    method_of_payment = models.CharField(max_length=2, choices=METHOD_OF_PAYMENT_TYPE, default='PS')
    status = models.CharField(max_length=2, choices=STATUS_TYPE, default='OH')

    #payer information
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=15)
    phone = models.CharField(max_length=15,blank=True,null=True)

    total_cost = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))

    #time information
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email.email + ' - ' + str(self.time_created)[0:19]

class PaymentItem(models.Model):
    article_id = models.ForeignKey('Article', to_field='id', on_delete=models.CASCADE, related_name='item_article')
    payment_order_id = models.ForeignKey('PaymentOrder', to_field='id', on_delete=models.CASCADE, related_name='items')
    
    user_discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],)
    
    number_of_pieces = models.PositiveIntegerField(default=1)
    article_price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    article_attributes = models.TextField(blank=True,null=True)

    valid = models.CharField(max_length=2, choices=VALID_TYPE, default="0")
    class Meta:
        verbose_name = "Payment item"
        verbose_name_plural = "Payment items"

    def amount(self):
        return str(self.number_of_pieces) + ' ' + self.article_id.unit_of_measure

class PaymentOrderCommentHistory(models.Model):
    payment_order_id = models.ForeignKey('PaymentOrder', to_field='id', on_delete=models.CASCADE, related_name='payment_comment')
    status = models.CharField(max_length=2, choices=STATUS_TYPE)
    comment = models.TextField(max_length=300, null=True, blank=True)
    created_by = models.ForeignKey('account.Account', to_field='email', on_delete=models.CASCADE, related_name='created_by')
    time_created = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Payment order comment"
        verbose_name_plural = "Payment order comments"
