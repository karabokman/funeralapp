# Generated by Django 4.1 on 2022-09-27 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_transaction_description_alter_transaction_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='description',
        ),
    ]
