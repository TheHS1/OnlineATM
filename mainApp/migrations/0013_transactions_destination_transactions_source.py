# Generated by Django 5.0.3 on 2024-05-02 16:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0012_rename_newid_accounts_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='destination',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='destination', to='mainApp.accounts'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactions',
            name='source',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='source', to='mainApp.accounts'),
            preserve_default=False,
        ),
    ]
