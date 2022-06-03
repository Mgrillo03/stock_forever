from unicodedata import name
from django.urls import URLPattern, path
from . import views


app_name = 'purchases'


urlpatterns = [
    #ex: /purchases/
    path("",  views.index, name= "index"),
    #ex: /purchases/5/update_saved/
    path("<int:purchase_id>/update/saved", views.save_update, name= "save_update"), 
    #ex /purchases/5/update/add
    path("<int:purchase_id>/update/add/", views.update_add, name="update_add"),
    #ex /purchases/5/update/del
    path("<int:purchase_id>/update/del/", views.update_del, name="update_del"),
    #ex: /purchases/5/detail-update-delete/   
    path("detail-update-delete/",  views.detail_update_delete, name= "detail_update_delete"),
    #ex: /purchases/5/detail/
    path("<int:purchase_id>/detail/", views.detail, name="detail"),   
    #ex: /purchases/new     
    path("new/1", views.new_1, name="new_1"),
    path("new/2", views.new_2, name="new_2"),
    #ex /purchases/add
    path("new/added/",views.add, name= "add"),
    #ex /purchases/5/product_deleted
    path("<int:purchase_id>/product-deleted", views.confirm_detele, name="confirm_delete")
    
]
