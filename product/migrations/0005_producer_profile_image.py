# Generated by Django 3.0.5 on 2020-05-12 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20200506_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='producer',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='producer_img/'),
        ),
    ]