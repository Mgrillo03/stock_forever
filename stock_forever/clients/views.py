from cgitb import reset
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


from .models import Client


def index(request):
    clients_list = Client.objects.all()
    return render(request, "clients/index.html",{
        'clients_list' : clients_list
    })

def new(request):
    return render(request, "clients/new.html",{})

def add(request): 
    client = Client()
    client.name = request.POST["name"]
    client.address = request.POST["address"]
    if request.POST["tlf"]:
        client.tlf = request.POST["tlf"]
    if request.POST["debt"]:
        client.debt = request.POST["debt"]
    client.save()

    return render(request, "clients/add.html",{
        'client':client
    })
    

def update_or_delete(request):
    clients_list = Client.objects.all()
    try:
        client = get_object_or_404(Client, pk=request.POST["choice"])
    except (KeyError, Client.DoesNotExist):
                return render(request, "clients/index.html", {
                    'clients_list':clients_list,
                    "error_message": "No elegiste un cliente"
                })
    else:

        if request.POST["action"] == "Editar":
            return render(request, "clients/update.html",{
                'client' : client
            })
        elif request.POST["action"] == "Eliminar":
            return render(request, "clients/delete.html",{
                'client' : client
            })
        
def save_update(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    client.name = request.POST["name"]
    client.address = request.POST["address"]
    if request.POST["tlf"]:
        client.tlf = request.POST["tlf"]
    if request.POST["debt"]:
        client.debt = request.POST["debt"]
    client.save()
    return render(request, "clients/update_saved.html",{
        'client' : client
    })

def confirm_detele(request, client_id):
    if request.POST["action"] == "Eliminar":
        client = get_object_or_404(Client, pk=client_id)
        client.delete()
        return render(request, "clients/client_deleted.html",{})
    else:
        return HttpResponseRedirect(reverse("clients:index"))
