# Generated by Django 3.0.1 on 2020-04-25 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20200418_1840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='product_id',
        ),
        migrations.AddField(
            model_name='attribute',
            name='article_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='attribute_article', to='product.Article'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='unit_of_measure',
            field=models.CharField(choices=[('M', 'Meter'), ('K', 'Kilogram'), ('P', 'Piece')], default='P', max_length=1),
        ),
    ]
