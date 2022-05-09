from email import message
from itertools import product
from unicodedata import category
from urllib import response
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Product


def index(request):
    product_list = Product.objects.all()
    return render(request, "stock/index.html",{
        'product_list' : product_list
    })

def search(request):
    query = request.GET["search"]
    product_list = Product.objects.filter(name__contains=query)
    return render(request, "stock/index.html",{
        "product_list" : product_list
    })


def new(request):
    return render(request, "stock/new.html",{})

def add(request):
    #product_list = Product.objects.all()    
    product = Product()
    product.name = request.POST["name"]
    product.category = request.POST["category"]
    product.material = request.POST["material"]
    product.stock = request.POST["in_stock"]
    product.price = request.POST["price"]
    if request.POST["sell_price"]:
        product.sell_price = request.POST["sell_price"]
    else: 
        product.sell_price = 0
    product.sug_price = float(product.price) * 2
    product.save()


    return render(request, "stock/add.html",{
        'product':product
    })
    
def save_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.name = request.POST["name"]
    product.category = request.POST["category"]
    product.material = request.POST["material"]
    product.stock = request.POST["in_stock"]
    product.price = request.POST["price"]
    product.sell_price = request.POST["sell_price"]
    product.sug_price = request.POST["sug_price"]
    product.save()
    return render(request, "stock/update_saved.html",{
        'product' : product
    })

def update_or_delete(request):
    product_list = Product.objects.all()
    try:
        product = get_object_or_404(Product, pk=request.POST["choice"])
    except (KeyError, Product.DoesNotExist):
                return index(request)
                # return render(request, "stock/index.html", {
                #     'product_list':product_list,
                #     "error_message": "No elegiste un articulo"
                # })
    else:

        if request.POST["action"] == "Editar":
            return render(request, "stock/update.html",{
                'product' : product
            })
        elif request.POST["action"] == "Eliminar":
            return render(request, "stock/delete.html",{
                'product' : product
            })

def confirm_detele(request, product_id):
    if request.POST["action"] == "Eliminar":
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        return render(request, "stock/product_deleted.html",{})
    else:
        return HttpResponseRedirect(reverse("stock:index"))
