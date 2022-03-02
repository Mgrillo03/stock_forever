from unicodedata import name
from django.urls import URLPattern, path
from . import views


app_name = 'supplier'

urlpatterns = [
    #ex: /supplier/
    path("",  views.index, name= "index"),
    #ex: /supplier/5/update_saved/
    path("<int:supplier_id>/update/saved", views.save_update, name= "save_update"),
    #ex: /supplier/5/delete/   falta actualizar
    path("update-delete/",  views.update_or_delete, name= "update_or_delete"),
    #ex: /supplier/new     falta actualizar
    path("new/", views.new, name="new"),
    #ex /supplier/add
    path("new/added/",views.add, name= "add"),
    #ex /supplier/5/product_deleted
    path("<int:supplier_id>/supplier-deleted", views.confirm_detele, name="confirm_delete")
    
]