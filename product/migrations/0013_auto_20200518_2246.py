# Generated by Django 3.0.5 on 2020-05-18 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20200517_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentorder',
            name='status',
            field=models.CharField(choices=[('DR', 'Draft'), ('IN', 'In the processing'), ('RE', 'Rejected'), ('RW', 'Rejected with counter offer'), ('WF', 'Waiting for payment'), ('SS', 'Shipment sent'), ('PD', 'Products delivered')], default='DR', max_length=2),
        ),
    ]
