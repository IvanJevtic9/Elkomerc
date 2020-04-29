# Generated by Django 3.0.1 on 2020-04-29 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_category', '0002_auto_20200426_1253'),
        ('product', '0010_auto_20200425_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='product_id',
        ),
        migrations.AddField(
            model_name='article',
            name='sub_category_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='article', to='product_category.SubCategory'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='unit_of_measure',
            field=models.CharField(choices=[('M', 'Meter'), ('K', 'Kilogram'), ('P', 'Piece')], default='P', max_length=1),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
