# Generated by Django 3.0.5 on 2020-05-23 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_auto_20200521_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentorder',
            name='attribute_notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paymentorder',
            name='note',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]
