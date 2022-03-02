from cgitb import reset
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


from .models import Supplier


def index(request):
    supplier_list = Supplier.objects.all()
    return render(request, "supplier/index.html",{
        'supplier_list' : supplier_list
    })

def new(request):
    return render(request, "supplier/new.html",{})

def add(request): 
    supplier = Supplier()
    supplier.name = request.POST["name"]
    supplier.address = request.POST["address"]
    if request.POST["tlf"]:
        supplier.tlf = request.POST["tlf"]
    if request.POST["debt"]:
        supplier.debt = request.POST["debt"]
    supplier.save()

    return render(request, "supplier/add.html",{
        'supplier':supplier
    })
    

def update_or_delete(request):
    supplier_list = Supplier.objects.all()
    try:
        supplier = get_object_or_404(Supplier, pk=request.POST["choice"])
    except (KeyError, Supplier.DoesNotExist):
                return render(request, "supplier/index.html", {
                    'supplier_list':supplier_list,
                    "error_message": "No elegiste un proveedor"
                })
    else:

        if request.POST["action"] == "Editar":
            return render(request, "supplier/update.html",{
                'supplier' : supplier
            })
        elif request.POST["action"] == "Eliminar":
            return render(request, "supplier/delete.html",{
                'supplier' : supplier
            })
        
def save_update(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    supplier.name = request.POST["name"]
    supplier.address = request.POST["address"]
    if request.POST["tlf"]:
        supplier.tlf = request.POST["tlf"]
    if request.POST["debt"]:
        supplier.debt = request.POST["debt"]
    supplier.save()
    return render(request, "supplier/update_saved.html",{
        'supplier' : supplier
    })

def confirm_detele(request, supplier_id):
    if request.POST["action"] == "Eliminar":
        supplier = get_object_or_404(Supplier, pk=supplier_id)
        supplier.delete()
        return render(request, "supplier/supplier_deleted.html",{})
    else:
        return HttpResponseRedirect(reverse("supplier:index"))
