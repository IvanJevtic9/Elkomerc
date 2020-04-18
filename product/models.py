from django.db import models

# Create your models here.

class Producer(models.Model):
    producer_name = models.CharField(max_length=30,unique=True)
    link = models.TextField(max_length=50,blank=True,null=True)
    description = models.TextField(max_length=100,blank=True,null=True)

    class Meta:
        verbose_name = "Producer"
        verbose_name_plural = "Producers"

    def __str__(self):
        return self.producer_name

class ProducerImage(models.Model):
    producer_id = models.ForeignKey('Producer',to_field='id',on_delete=models.CASCADE,related_name='producer_image')
    image = models.ImageField(upload_to='producer_img/')
    image_name = models.CharField(max_length=30,blank=True,null=True)
    content_type = models.CharField(max_length=20,blank=True,null=True)
    size = models.IntegerField(blank=True,null=True)
    height = models.IntegerField(blank=True,null=True)
    width = models.IntegerField(blank=True,null=True)
    purpose = models.CharField(max_length=20,blank=True,null=True)

    class Meta:
        verbose_name = "Producer image"
        verbose_name_plural = "Producer images"

    def __str__(self):
        return self.image_name

class Program(models.Model):
    program_name = models.CharField(max_length=30)
    producer_id = models.ForeignKey('Producer',to_field='id',on_delete=models.CASCADE,related_name='program')

    class Meta:
        verbose_name = "Program"
        verbose_name_plural = "Programs"

    def __str__(self):
        return self.program_name

class Product(models.Model):
    MEASURE_TYPE = (
        ("M","Meter"),
        ("P","Piece")
    )

    product_name = models.CharField(max_length=60)
    description = models.TextField(max_length=100,blank=True,null=True)
    unit_of_measure = models.CharField(max_length=1,choices=MEASURE_TYPE,default="P")
    sub_category_id = models.ForeignKey('product_category.SubCategory',to_field='id',on_delete=models.CASCADE,related_name='product')

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.product_name

class Attribute(models.Model):
    product_id = models.ForeignKey('Product',to_field='id',on_delete=models.CASCADE,related_name='attribute_product')
    feature_id = models.ForeignKey('product_category.Feature',to_field='id',on_delete=models.CASCADE,related_name='attribute_feature')
    value = models.TextField(max_length=30)

    class Meta:
        verbose_name = "Attribute"
        verbose_name_plural = "Attributes"

    def __str__(self):
        return self.feature_id.feature_name

class Article(models.Model):
    CURRENCY_TYPE = (
        ('RSD', 'Dinar'),
        ('EUR', 'Euro')
    )

    product_id = models.ForeignKey('Product',to_field='id',on_delete=models.CASCADE,related_name='article')
    price = models.DecimalField(max_digits=20,decimal_places=2)
    currency = models.CharField(max_length=3,choices=CURRENCY_TYPE,default='RSD')
    program_id = models.ForeignKey('Program', to_field='id',on_delete=models.CASCADE,blank=True,null=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.product_id.product_name    

class ArticleImage(models.Model):
    article_id = models.ForeignKey('Article', to_field='id',on_delete=models.CASCADE,related_name='image')
    image = models.ImageField(upload_to='article_img/')
    image_name = models.CharField(max_length=30,blank=True,null=True)
    content_type = models.CharField(max_length=20,blank=True,null=True)
    size = models.IntegerField(blank=True,null=True)
    height = models.IntegerField(blank=True,null=True)
    width = models.IntegerField(blank=True,null=True)
    purpose = models.CharField(max_length=20,blank=True,null=True)

    class Meta:
        verbose_name = "Article image"
        verbose_name_plural = "Article images"

    def __str__(self):
        return self.image_name