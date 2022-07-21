from django.db import models


from clients.models import Client
from stock.models import Product

class Sell(models.Model):
    client = models.ForeignKey(
            Client, 
            on_delete= models.CASCADE,
            null=False, 
            blank= False
    )
    sell_date = models.DateTimeField(auto_now_add=True)
    product = models.ManyToManyField(
        Product,
        through='Sell_Product',
        blank=True
    )
    total = models.FloatField(default=0)


class Sell_Product(models.Model):
    sell = models.ForeignKey(
        Sell,
        on_delete= models.CASCADE,
        null=False,
        blank=False
    )
    product = models.ForeignKey(
        Product,
        on_delete= models.CASCADE,
        null=False,
        blank=False
    )
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0)
    total = models.FloatField(default=0)