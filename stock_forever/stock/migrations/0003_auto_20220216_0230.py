# Generated by Django 3.2.12 on 2022-02-16 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_auto_20220216_0228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='categoria',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='material',
            field=models.CharField(max_length=50),
        ),
    ]
