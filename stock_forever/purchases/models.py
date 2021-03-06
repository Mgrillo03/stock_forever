from django.db import models


from supplier.models import Supplier
from stock.models import Product

class Purchase(models.Model):
    supplier = models.ForeignKey(
            Supplier, 
            on_delete= models.CASCADE,
            null= False, 
            blank= False,
    )
    purchase_date = models.DateTimeField(auto_now_add=True)
    product = models.ManyToManyField(
        Product,
        through='Purchase_Product',
        blank=True
    )
    total = models.FloatField(default=0) 


class Purchase_Product(models.Model):
    purchase = models.ForeignKey(
        Purchase,
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