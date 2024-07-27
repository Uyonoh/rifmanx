# Generated by Django 5.0.6 on 2024-07-26 21:07

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        ('drugs', '0017_delete_sale'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessMonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opening_cash', models.FloatField()),
                ('opening_stock', models.IntegerField()),
                ('opening_date', models.DateField(default=datetime.date(2024, 7, 26))),
                ('closing_cash', models.FloatField(null=True)),
                ('closing_stock', models.IntegerField(null=True)),
                ('closing_date', models.DateField(null=True)),
                ('margin', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
                ('price', models.FloatField()),
                ('date', models.DateField(default=datetime.date(2024, 7, 26))),
            ],
        ),
        migrations.CreateModel(
            name='Debit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
                ('price', models.FloatField()),
                ('date', models.DateField(default=datetime.date(2024, 7, 26))),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('price', models.FloatField()),
                ('date', models.DateField(default=datetime.date(2024, 7, 26))),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drugs.drug')),
            ],
        ),
    ]
