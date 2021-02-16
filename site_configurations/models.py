from django.db import models
from decimal import Decimal

class Corosel(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=150,blank=True,null=True)
    link = models.CharField(max_length=100,null=True,blank=True)
    corosel_image = models.ImageField(upload_to='corosel_img/', blank=True,null=True)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Corosel'
        verbose_name_plural = 'Corosels'

