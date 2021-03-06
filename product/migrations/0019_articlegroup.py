# Generated by Django 3.0.5 on 2020-05-31 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_auto_20200531_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('article_ids', models.ManyToManyField(to='product.Article')),
            ],
            options={
                'verbose_name': 'Article group',
                'verbose_name_plural': 'Article groups',
            },
        ),
    ]
