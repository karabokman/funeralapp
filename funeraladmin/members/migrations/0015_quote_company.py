# Generated by Django 4.1 on 2022-09-29 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0014_remove_quote_identity_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='company',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
