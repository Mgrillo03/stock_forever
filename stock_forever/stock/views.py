from unicodedata import category
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Product


def index(request, added=''):
    product_list = Product.objects.all()
    return render(request, "stock/index.html",{
        'product_list' : product_list,
        'added': added
    })

def new(request):
    return render(request, "stock/new.html",{})

def add(request):
    #product_list = Product.objects.all()    
    product = Product()
    product.name = request.POST["name"]
    product.category = request.POST["category"]
    product.material = request.POST["material"]
    product.in_stock = request.POST["in_stock"]
    product.price = request.POST["price"]
    if request.POST["sell_price"]:
        product.sell_price = request.POST["sell_price"]
    else: 
        product.sell_price = 0
    product.sug_price = float(product.price) * 2
    product.save()


    return render(request, "stock/add.html",{
        'name' : product.name,
        'category': product.category,
        'material': product.material,
        'in_stock' : product.in_stock,
        'price' : product.price,
        'sell_price' : product.sell_price,
        'sug_price' : product.sug_price
    })