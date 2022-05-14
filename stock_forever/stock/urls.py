from unicodedata import name
from django.urls import URLPattern, path
from . import views


app_name = 'stock'

urlpatterns = [
    #ex: /stock/
    path("",  views.index, name= "index"),
    #ex: /stock/search/
    path("search/", views.search, name="search"),
    #ex: /stock/5/
    #path("<int:pk>/",  views.DetailView.as_view(), name= "detail"),
    #ex: /stock/5/update/   falta actualizar
    #path("<int:product_id>/update/",  views.update, name= "update"),
    #ex: /stock/5/update_saved/
    path("<int:product_id>/update/saved", views.save_update, name= "save_update"),
    #ex: /stock/5/delete/   falta actualizar
    path("update-delete/",  views.update_or_delete, name= "update_or_delete"),
    #ex: /stock/new     falta actualizar
    path("new/", views.new, name="new"),
    #ex /stock/add
    path("new/added/",views.add, name= "add"),
    #ex /stock/5/product_deleted
    path("<int:product_id>/product-deleted", views.confirm_detele, name="confirm_delete")
    
]