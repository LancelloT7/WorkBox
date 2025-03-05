from django.urls import path
from . import views

urlpatterns = [

    path('cad_sku_sufixo/', views.cad_sku_sufixo, name='cad_sku_sufixo'),
    #path('cadastrar_sufixo/', views.cad_sufixo, name='cad_sufixo'),
]