# Generated by Django 3.0.5 on 2020-05-17 03:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0007_paymentitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentitem',
            name='email',
        ),
        migrations.CreateModel(
            name='PaymentOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_email', to=settings.AUTH_USER_MODEL, to_field='email')),
                ('payment_item_id', models.ManyToManyField(to='product.PaymentItem')),
            ],
        ),
    ]
