# Generated by Django 3.0.5 on 2021-04-10 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_auto_20210410_2206'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymentordercommenthistory',
            options={'verbose_name': 'Payment order comment', 'verbose_name_plural': 'Payment order comments'},
        ),
        migrations.AddField(
            model_name='paymentordercommenthistory',
            name='payment_order_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='payment_comment', to='product.PaymentOrder'),
            preserve_default=False,
        ),
    ]