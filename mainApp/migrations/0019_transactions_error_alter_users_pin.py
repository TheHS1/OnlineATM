# Generated by Django 5.0.3 on 2024-05-09 17:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0018_accounts_date_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='error',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='pin',
            field=models.CharField(default='', max_length=4, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
    ]