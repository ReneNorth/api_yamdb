# Generated by Django 2.2.28 on 2022-10-31 08:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0016_auto_20221027_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(2022)]),
        ),
    ]
