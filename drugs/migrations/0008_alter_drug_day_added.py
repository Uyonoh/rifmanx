# Generated by Django 5.0.6 on 2024-07-24 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0007_alter_drug_day_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug',
            name='day_added',
            field=models.DateField(default='2024-07-24'),
        ),
    ]
