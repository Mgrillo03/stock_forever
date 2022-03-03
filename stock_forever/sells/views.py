from cgitb import reset
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


from .models import Sell


def index(request):
    sells_list = Sell.objects.all()
    return render(request, "sells/index.html",{
        'sells_list' : sells_list
    })

def new(request):
    return render(request, "sells/new.html",{})

def add(request): 
    sell = Sell()
    sell.name = request.POST["name"]
    sell.address = request.POST["address"]
    if request.POST["tlf"]:
        sell.tlf = request.POST["tlf"]
    if request.POST["debt"]:
        sell.debt = request.POST["debt"]
    sell.save()

    return render(request, "sells/add.html",{
        'sell':sell
    })
    

def update_or_delete(request):
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
        return render(request, "sells/client_deleted.html",{})
    else:
        return HttpResponseRedirect(reverse("sells:index"))
