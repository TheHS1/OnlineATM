# Generated by Django 5.0.3 on 2024-03-21 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_alter_users_address_alter_users_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(default='@.com', max_length=200),
        ),
    ]
