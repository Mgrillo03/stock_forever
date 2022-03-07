from cgitb import reset
from http import client
from itertools import product
import re
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


from .models import Sell, Sell_Product
from stock.models import Product
from clients.models import Client



def index(request):
    sells_list = Sell.objects.all()
    
    return render(request, "sells/index.html",{
        'sells_list' : sells_list
    })


def detail(request, sell_id):
    pass



def new_1(request):
    clients_list = Client.objects.all()
     
    return render(request, "sells/new_1.html",{
        'clients_list' : clients_list   
    })

def new_2(request):
    clients_list = Client.objects.all()
    products_list = Product.objects.all()
    product_quantity = request.POST["quantity"]
    if request.POST["client"]:
        client_name = request.POST["client"]
    else: 
        client_name = ""
    quantity = request.POST["quantity"]
    quantity_list = range(int(quantity))
    return render(request, "sells/new_2.html",{
        'clients_list' : clients_list,
        'client_name' : client_name,
        'products_list' : products_list,
        'quantity_list' : quantity_list,
        'product_quantity' : product_quantity
        
    })

def add(request): 
    client_name = request.POST["client"]
    client = Client.objects.get(name=client_name)
    sell = Sell.objects.create(client=client)
    sell.save()
    product_quantity = request.POST["product_quantity"]
    suma=0
    for i in range(int(product_quantity)):
        var = "product_"+str(i+1)
        name = request.POST[var]
        product = Product.objects.get(name=name)
        
        var = "quantity_"+str(i+1)
        quantity = request.POST[var]

        var = "price_"+str(i+1)
        price = request.POST[var]
        
        total = float(quantity) * float(price)
        suma+=total

        sell.product.add(product, through_defaults={'price':price,'quantity':quantity, 'total':total})

    sell.total = suma
    sell.save()
    products_list = sell.sell_product_set.all()


    return render(request, "sells/add.html",{
        'sell':sell,
        'products_list': products_list
    })
    

def detail_update_delete(request):    
    sells_list = Sell.objects.all()
    try:
        sell = get_object_or_404(Sell, pk=request.POST["choice"])
    except (KeyError, Sell.DoesNotExist):
                return render(request, "sells/index.html", {
                    'sells_list':sells_list,
                    "error_message": "No elegiste una venta"
                })
    else:

        if request.POST["action"] == "Editar":
            return render(request, "sells/update.html",{
                'sell' : sell
            })
        elif request.POST["action"] == "Eliminar":
            return render(request, "sells/delete.html",{
                'sell' : sell
            })
        elif request.POST["action"] == "Detalle":
            sell_product_set = sell.sell_product_set.all()
            return render(request, "sells/detail.html",{
                'sell': sell,
                'sell_product_set': sell_product_set
            })


            
        
def save_update(request, sell_id):
    sell = get_object_or_404(Sell, pk=sell_id)
    sell.name = request.POST["name"]
    sell.address = request.POST["address"]
    if request.POST["tlf"]:
        sell.tlf = request.POST["tlf"]
    if request.POST["debt"]:
        sell.debt = request.POST["debt"]
    sell.save()
    return render(request, "sells/update_saved.html",{
        'sell' : sell
    })

def confirm_detele(request, sell_id):
    if request.POST["action"] == "Eliminar":
        sell = get_object_or_404(Sell, pk=sell_id)
        sell.delete()
        return render(request, "sells/sell_deleted.html",{})
    else:
        return HttpResponseRedirect(reverse("sells:index"))
