# Generated by Django 5.0.6 on 2024-07-29 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_businessmonth_opening_date_alter_credit_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessmonth',
            name='margin',
        ),
    ]
