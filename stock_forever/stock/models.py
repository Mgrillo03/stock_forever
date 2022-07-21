from django.db import models

class Product(models.Model):
    """ Product main model
    name : product description or name
    category : product category
    material : product material
    price : product cost
    stock : quantity available 
    sug_price : suggested sell price
    sell_price : real sell price

    """
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    material = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    stock = models.IntegerField(default=0)
    sug_price = models.FloatField(default=price)
    sell_price = models.FloatField(default= sug_price)

    def __str__(self) :
        return self.name
