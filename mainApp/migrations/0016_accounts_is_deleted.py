# Generated by Django 5.0.3 on 2024-05-08 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0015_users_date_opened'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='is_deleted',
            field=models.BooleanField(default=True),
        ),
    ]
