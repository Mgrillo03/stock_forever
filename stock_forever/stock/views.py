from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


def index(request):
    product_list = Product.objects.all()
    return render(request, "stock/index.html",{
        'product_list' : product_list
    })