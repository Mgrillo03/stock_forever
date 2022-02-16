from unicodedata import name
from django.urls import URLPattern, path
from . import views


app_name = 'stock'

urlpatterns = [
    #ex: /stock/
    path("",  views.index, name= "index"),
    #ex: /stock/5/
    #path("<int:pk>/",  views.DetailView.as_view(), name= "detail"),
    #ex: /stock/5/update/   falta actualizar
    #path("<int:pk>/update/",  views.ResultView.as_view(), name= "update"),
    #ex: /stock/5/delete/   falta actualizar
    #path("<int:question_id>/vote/",  views.vote, name= "delete"),
    #ex: /stock/add     falta actualizar
    #path("stock/add/", name="add")
]