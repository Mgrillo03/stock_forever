from unicodedata import name
from django.urls import URLPattern, path
from . import views


app_name = 'clients'

urlpatterns = [
    #ex: /clients/
    path("",  views.index, name= "index"),
    #ex: /clients/5/update_saved/
    path("<int:client_id>/update/saved", views.save_update, name= "save_update"),
    #ex: /clients/5/delete/   falta actualizar
    path("update-delete/",  views.update_or_delete, name= "update_or_delete"),
    #ex: /clients/new     falta actualizar
    path("new/", views.new, name="new"),
    #ex /clients/add
    path("new/added/",views.add, name= "add"),
    #ex /clients/5/product_deleted
    path("<int:client_id>/client-deleted", views.confirm_detele, name="confirm_delete")
    
]