# Generated by Django 3.0.5 on 2020-05-21 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20200516_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='parent_comment_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_comment', to='account.Comments'),
        ),
    ]
