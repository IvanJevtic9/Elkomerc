from django.db import models

# Create your models here.

class Producer(models.Model):
    producer_name = models.CharField(max_length=30,unique=True)
    link = models.TextField(max_length=50,blank=True,null=True)
    profile_image = models.ImageField(upload_to='producer_img/',blank=True,null=True)
    description = models.TextField(max_length=100,blank=True,null=True)

    class Meta:
        verbose_name = "Producer"
        verbose_name_plural = "Producers"

    def __str__(self):
        return self.producer_name

class Attribute(models.Model):
    article_id = models.ForeignKey('Article',to_field='id',on_delete=models.CASCADE,related_name='attribute_article')
    feature_id = models.ForeignKey('product_category.Feature',to_field='id',on_delete=models.CASCADE,related_name='attribute_feature')
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
        ("M","Meter"),
        ("K", "Kilogram"),
        ("P","Piece")
    )

    article_code = models.CharField(max_length=15,unique=True)
    article_name = models.CharField(max_length=80)
    sub_category_id = models.ForeignKey('product_category.SubCategory',to_field='id',on_delete=models.CASCADE,related_name='article')
    producer_id = models.ForeignKey('Producer', to_field='id',on_delete=models.CASCADE,blank=True,null=True,related_name='article_producer')
    product_group_id = models.ForeignKey('ProductGroup', to_field='id',on_delete=models.CASCADE,related_name='article_group')

    price = models.DecimalField(max_digits=20,decimal_places=2)
    currency = models.CharField(max_length=3,choices=CURRENCY_TYPE,default='RSD')
    unit_of_measure = models.CharField(max_length=1,choices=MEASURE_TYPE,default="P")
    description = models.TextField(max_length=200,blank=True,null=True)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.article_name    

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