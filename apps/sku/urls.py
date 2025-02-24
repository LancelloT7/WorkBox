from django.urls import path
from . import views

urlpatterns = [

    path('cadastrar_sku/', views.cad_sku, name='cad_sku'),
    path('cadastrar_sufixo/', views.cad_sufixo, name='cad_sufixo'),
]