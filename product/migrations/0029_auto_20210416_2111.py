# Generated by Django 3.0.5 on 2021-04-16 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0028_auto_20210416_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentordercommenthistory',
            name='status',
            field=models.IntegerField(choices=[(0, 'NA_CEKANJU'), (1, 'U_OBRADI'), (2, 'ODBIJENO'), (3, 'MODIFIKOVANO'), (4, 'ODOBRENO_ZA_SLANJE'), (5, 'POSLATO'), (6, 'VRACENA'), (7, 'ISPORUCENJA')]),
        ),
    ]
