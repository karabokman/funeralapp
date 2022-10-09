# Generated by Django 4.1 on 2022-09-26 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_alter_memberproduct_covered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='Zip_code',
        ),
        migrations.RemoveField(
            model_name='member',
            name='address',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.member'),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('province', models.CharField(max_length=100)),
                ('zip', models.CharField(max_length=100)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.member')),
            ],
        ),
    ]