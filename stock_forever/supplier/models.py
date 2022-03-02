from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    tlf = models.CharField(max_length=15, default='')
    debt = models.FloatField(default=0)
    address = models.CharField(max_length=100)

    def __str__(self) :
        return self.name