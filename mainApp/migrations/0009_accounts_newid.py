# Generated by Django 5.0.3 on 2024-05-02 16:17

import mainApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0008_alter_accounts_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='newid',
            field=models.IntegerField(default=mainApp.models.Accounts.generateID),
        ),
    ]
