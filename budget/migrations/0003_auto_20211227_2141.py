# Generated by Django 3.2.6 on 2021-12-27 15:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_auto_20211012_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenditure',
            name='sum',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='expenditure',
            name='updated_at',
            field=models.DateField(default=datetime.date.today, verbose_name='Update Date'),
        ),
    ]