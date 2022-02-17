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
    product_list = Product.objects.all()
    added="Product Added Succesfully"
    #opcion = request.GET["category"]
    price = request.POST["price"]
    opcion = request.POST["category"]
    return render(request, "stock/add.html",{
        'product_list' : product_list,
        'added': "added succesfully",
        "opcion":opcion,
        "price": price

    })