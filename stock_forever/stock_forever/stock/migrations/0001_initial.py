# Generated by Django 3.2.12 on 2022-02-16 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('price', models.FloatField(default=0)),
                ('stock', models.IntegerField(default=0)),
                ('sug_price', models.FloatField(default=models.FloatField(default=0))),
                ('sell_price', models.FloatField(default=models.FloatField(default=models.FloatField(default=0)))),
            ],
        ),
    ]