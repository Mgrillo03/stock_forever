from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone


from .models import Sell
from stock.models import Product
from clients.models import Client

import datetime

def date_format(date):
    """ date_format 
        date type: datetime.date 
        
        format datetime.date into '%Y-%m-%d' 
        adding 0 if de day or month are < 10 
    """
    date_start = str(date.year)
    if date.month < 10:
        date_start += '-0'+ str(date.month)
    else:
        date_start += '-'+ str(date.month)
    if date.day < 10:
        date_start += '-0'+ str(date.day)
    else:
        date_start += '-'+ str(date.day)
    return date_start
        

def index(request):
    sells_list = Sell.objects.all()
    
    return render(request, "sells/index.html",{
        'sells_list' : sells_list
    })

def new_1(request, error_message = ''):
    clients_list = Client.objects.all()
     
    return render(request, "sells/new.html",{
        'clients_list' : clients_list,
        'error_message': error_message,
        'cond' : True
    })

def new_2(request):
    products_list = Product.objects.all()
    product_quantity = request.POST["quantity"]
    client_name = request.POST["client"]
    quantity_list = range(int(product_quantity))

    try:
        client = Client.objects.get(name=client_name)
    except (KeyError, Client.DoesNotExist):
                error_message = 'El cliente ingresano no existe en la base de datos'
                return new_1(request,error_message=error_message)
    else:

        return render(request, "sells/new.html",{        
            'client_name' : client_name,
            'products_list' : products_list,
            'quantity_list' : quantity_list,
            'product_quantity' : product_quantity,
            'cond' : False        
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
        product.stock -= int(quantity)
        product.save()

        var = "price_"+str(i+1)
        price = request.POST[var]
        
        total = float(quantity) * float(price)
        suma+=total

        sell.product.add(product, through_defaults={'price':price,'quantity':quantity, 'total':total})

    sell.total = suma
    sell.save()
    products_list = sell.sell_product_set.all()

    payed = request.POST["payed"]
    substraction = suma - float(payed)
    client.debt += substraction
    client.save()

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
            products_list = Product.objects.all()
            clients_list = Client.objects.all()
            sell_product_set = sell.sell_product_set.all()

            return render(request, "sells/update.html",{
                'sell' : sell,
                'products_list' : products_list,
                'clients_list' : clients_list,
                'sell_product_set' : sell_product_set

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

def detail(request, sell_id):
    sell = get_object_or_404(Sell, pk=sell_id)
    sell_product_set = sell.sell_product_set.all()
    return render(request, "sells/detail.html",{
        'sell': sell,
        'sell_product_set': sell_product_set
    })

def update_add(request, sell_id):
    sell = get_object_or_404(Sell, pk=sell_id)
    products_list = Product.objects.all()
    sell_products = sell.product.all()
    for i in products_list:
        if i not in sell_products:
            sell.product.add(i)
            break    
    sell.save()
    clients_list = Client.objects.all()
    sell_product_set = sell.sell_product_set.all()

    return render(request, "sells/update.html",{
        'sell' : sell,
        'products_list' : products_list,
        'clients_list' : clients_list,
        'sell_product_set' : sell_product_set

    })

def update_del(request, sell_id):
    sell = get_object_or_404(Sell, pk=sell_id)
    clients_list = Client.objects.all()
    products_list = Product.objects.all()
    last_product = sell.product.last()   
    sell.product.remove(last_product)
    sell.save()    
    sell_product_set = sell.sell_product_set.all()

    return render(request, "sells/update.html",{
        'sell' : sell,
        'products_list' : products_list,
        'clients_list' : clients_list,
        'sell_product_set' : sell_product_set

    })

def save_update(request, sell_id):
    sell = get_object_or_404(Sell, pk=sell_id)
    client_name = request.POST["client"]
    client = get_object_or_404(Client, name= client_name)
    sell.client = client
    sell.save()

    set_product = sell.sell_product_set.all()

    products_totals = sell.product.count()
    products_list = []
    
    for i in range(products_totals):
        product_old = get_object_or_404(Product, pk = set_product[i].product.pk)
        product_old.stock += set_product[i].quantity
        product_old.save()

        var = 'product_'+str(i+1)
        name = request.POST[var]
        product = get_object_or_404(Product, name = name)
        products_list.append(product)

        

    sell.product.set(products_list)
    suma = 0

    for i in range(products_totals):
        var = 'product_'+str(i+1)
        name = request.POST[var]
        product = get_object_or_404(Product, name = name)
        sell_detail = sell.sell_product_set.get(product=product)
        var = 'quantity_'+str(i+1)
        quantity = request.POST[var]
        sell_detail.quantity = int(quantity)
        product.stock -= int(quantity)
        product.save()

        var = 'price_'+str(i+1)
        price = request.POST[var]
        sell_detail.price = float(price)
    
        total = float(price) * float(quantity)
        sell_detail.total = total
        sell_detail.save()

        suma += total   
    
    sell.total = suma
    
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


def metrics(request):
    sell_list = Sell.objects.filter(sell_date__gte = datetime.date(2022,7,20))
    total_sell = 0
    total_cost = 0
    sells_quantity = sell_list.count()

    for i in sell_list:
        total_sell += i.total
        product_quantity = i.sell_product_set.count()
        sell_set = i.sell_product_set.all()
        cost = 0
        for j in range(product_quantity):
            unit_cost = sell_set[j].product.price
            quantity = sell_set[j].quantity
            cost += unit_cost * quantity
        total_cost += cost

    earnings = total_sell - total_cost
    date = datetime.date.today()

    date_start = date_format(date)
    

        ### Calcular el total de todas las ventas en las fechas seleecionadas / Calcular el costo de cada articulo vendido
    
    return render(request, "sells/metrics.html",{
        'total_sell' : total_sell,
        'total_cost' : total_cost,
        'sells_quantity' : sells_quantity,
        'earnings' : earnings,
        'date_start' : date_start,
        'date_end' : date_start        
    })

def show_metrics(request):
    date_start = request.POST['start']
    date_end = request.POST['end']
    date_end_fixed = datetime.datetime.strptime(date_end,'%Y-%m-%d')
    date_end_fixed += datetime.timedelta(days=1)
    q1 = Sell.objects.filter(sell_date__gte = date_start)
    sell_list =  q1.filter(sell_date__lte=date_end_fixed)
    total_sell = 0
    total_cost = 0
    sells_quantity = sell_list.count()
    print(type(date_start),date_start)

    for i in sell_list:
        total_sell += i.total
        product_quantity = i.sell_product_set.count()
        sell_set = i.sell_product_set.all()
        cost = 0
        for j in range(product_quantity):
            unit_cost = sell_set[j].product.price
            quantity = sell_set[j].quantity
            cost += unit_cost * quantity
        total_cost += cost

    earnings = total_sell - total_cost
   
    
    
    return render(request, "sells/metrics.html",{
        'total_sell' : total_sell,
        'total_cost' : total_cost,
        'sells_quantity' : sells_quantity,
        'earnings' : earnings,
        'date_start' : date_start,
        'date_end' : date_end
        
    })