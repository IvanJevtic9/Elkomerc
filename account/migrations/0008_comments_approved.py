# Generated by Django 3.0.5 on 2020-05-30 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20200523_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
