# Generated by Django 5.0.6 on 2024-07-27 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0017_delete_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug',
            name='day_added',
            field=models.DateField(default='2024-07-27'),
        ),
    ]