# Generated by Django 5.0.3 on 2024-03-23 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_alter_users_email_alter_users_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='username',
        ),
    ]
