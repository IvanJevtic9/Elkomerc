# Generated by Django 3.0.5 on 2021-01-30 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Corosel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField(blank=True, max_length=150, null=True)),
                ('link', models.CharField(blank=True, max_length=100, null=True)),
                ('corosel_image', models.ImageField(blank=True, null=True, upload_to='corosel_img/')),
            ],
            options={
                'verbose_name': 'Corosel',
                'verbose_name_plural': 'Corosels',
            },
        ),
    ]