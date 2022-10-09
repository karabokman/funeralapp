# Generated by Django 4.1 on 2022-09-29 20:26

from django.db import migrations, models
import members.models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0012_alter_transaction_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quote',
            old_name='address',
            new_name='city',
        ),
        migrations.AddField(
            model_name='quote',
            name='province',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='quote',
            name='street',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='quote',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='quote',
            name='due',
            field=models.DateTimeField(default=members.models.tenDays),
        ),
        migrations.AlterField(
            model_name='quote',
            name='paid',
            field=models.DateTimeField(null=True),
        ),
    ]