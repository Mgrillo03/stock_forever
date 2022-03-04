from unicodedata import name
from django.urls import URLPattern, path
from . import views


app_name = 'sells'

urlpatterns = [
    #ex: /sells/
    path("",  views.index, name= "index"),
    #ex: /sells/5/update_saved/
    # path("<int:sell_id>/update/saved", views.save_update, name= "save_update"),
    # #ex: /sells/5/delete/   falta actualizar
    # path("update-delete/",  views.update_or_delete, name= "update_or_delete"),
    # #ex: /sells/new     falta actualizar
    path("new/1", views.new_1, name="new_1"),
    path("new/2", views.new_2, name="new_2"),
    # #ex /sells/add
    # path("new/added/",views.add, name= "add"),
    # #ex /sells/5/product_deleted
    # path("<int:sell_id>/product-deleted", views.confirm_detele, name="confirm_delete")
    
]