from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=30,unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    category_id = models.ForeignKey('Category',to_field='id',on_delete=models.CASCADE,related_name='sub_category')
    sub_category_name = models.CharField(max_length=30,unique=True)

    class Meta:
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return self.sub_category_name

class Feature(models.Model):
    DATA_TYPE = (
        ('INT','Integer'),
        ('STR', 'String'),
        ('DEC', 'Decimal'),
        ('BOL', 'Bolean'),
    )
    data_type = models.CharField(max_length=3,choices=DATA_TYPE,default='STR')
    feature_name = models.CharField(max_length=20,unique=True)

    class Model:
        verbose_name = "Feature"
        verbose_name_plural = "Features"

    def __str__(self):
        return self.feature_name     

class FloorFeature(models.Model):
    sub_category_id = models.ForeignKey('SubCategory',to_field='id',on_delete=models.CASCADE,related_name='floor_feture_cat')
    feature_id = models.ForeignKey('Feature',to_field='id',on_delete=models.CASCADE,related_name='floor_feature_fea')

    class Model:
        verbose_name = "Floor-Feature"
        verbose_name_plural = "Floor-Features"    