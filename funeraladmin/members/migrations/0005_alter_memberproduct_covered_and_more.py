# Generated by Django 4.1 on 2022-08-14 10:18

from django.db import migrations, models
import members.models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_rename_invoicedetails_invoicedetail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberproduct',
            name='Covered',
            field=models.DateField(verbose_name=members.models.six_month),
        ),
        migrations.AlterField(
            model_name='memberproduct',
            name='inception',
            field=models.DateField(auto_now_add=True),
        ),
    ]
