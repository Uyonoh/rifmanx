# Generated by Django 5.0.6 on 2024-07-25 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0013_sale_amount_sale_price_sale_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suspension',
            name='no_packs',
            field=models.IntegerField(default=10, null=True),
        ),
    ]