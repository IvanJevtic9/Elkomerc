# Generated by Django 3.0.5 on 2021-04-13 23:46

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0025_paymentordercommenthistory_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentorder',
            name='full_name',
            field=models.CharField(default='Ivan Jevtic', max_length=61),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paymentorder',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
