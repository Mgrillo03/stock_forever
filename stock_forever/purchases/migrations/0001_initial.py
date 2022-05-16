# Generated by Django 3.2.12 on 2022-05-16 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '0005_rename_nombre_product_name'),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('total', models.FloatField(default=0)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.client')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.product')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchases.purchase')),
            ],
        ),
        migrations.AddField(
            model_name='purchase',
            name='product',
            field=models.ManyToManyField(blank=True, through='purchases.Purchase_Product', to='stock.Product'),
        ),
    ]