# Generated by Django 4.1 on 2022-09-27 14:29

from django.db import migrations, models
import members.models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_remove_member_zip_code_remove_member_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='description',
            field=models.CharField(default='null', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='due',
            field=models.DateTimeField(default=members.models.tenDays),
        ),
    ]