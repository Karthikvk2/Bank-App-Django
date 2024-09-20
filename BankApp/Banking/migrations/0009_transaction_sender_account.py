# Generated by Django 5.1.1 on 2024-09-20 11:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Banking', '0008_remove_transaction_sender_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='sender_account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Banking.bankaccount'),
        ),
    ]
