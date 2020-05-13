# Generated by Django 3.0.5 on 2020-05-12 22:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_delete_producerimage'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='art_wishlist', to='product.Article')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acc_wishlist', to=settings.AUTH_USER_MODEL, to_field='email')),
            ],
            options={
                'verbose_name': 'Wish',
                'verbose_name_plural': 'WishList',
            },
        ),
        migrations.CreateModel(
            name='Stars',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='art_stars', to='product.Article')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acc_stars', to=settings.AUTH_USER_MODEL, to_field='email')),
            ],
            options={
                'verbose_name': 'Star',
                'verbose_name_plural': 'Stars',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=400)),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='art_comments', to='product.Article')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acc_comments', to=settings.AUTH_USER_MODEL, to_field='email')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
    ]
