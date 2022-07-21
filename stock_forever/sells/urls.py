from unicodedata import name
from django.urls import URLPattern, path
from . import views


app_name = 'sells'

urlpatterns = [
    #ex: /sells/
    path("",  views.index, name= "index"),
    #ex: /sells/5/update_saved/
    path("<int:sell_id>/update/saved", views.save_update, name= "save_update"), 
    #ex /sells/5/update/add
    path("<int:sell_id>/update/add/", views.update_add, name="update_add"),
    #ex /sells/5/update/del
    path("<int:sell_id>/update/del/", views.update_del, name="update_del"),
    #ex: /sells/5/detail-update-delete/   
    path("detail-update-delete/",  views.detail_update_delete, name= "detail_update_delete"),
    #ex: /sells/5/detail/
    path("<int:sell_id>/detail/", views.detail, name="detail"),   
    #ex: /sells/new     
    path("new/1", views.new_1, name="new_1"),
    path("new/2", views.new_2, name="new_2"),
    #ex /sells/add
    path("new/added/",views.add, name= "add"),
    #ex /sells/5/product_deleted
    path("<int:sell_id>/product-deleted", views.confirm_detele, name="confirm_delete"),
    #ex /sells/metrics
    path("metrics/", views.metrics, name="metrics"),
    #ex /metrics/show
    path("metrics/show/", views.show_metrics, name="show-metrics")

    
]