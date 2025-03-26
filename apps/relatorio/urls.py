from django.urls import path
from . import views

urlpatterns = [

    path('gerar_relatorio/', views.gerar_relatorio, name='gerar_relatorio'),
    path('gerar_ordem-de-servico/', views.gerar_os, name='gerar_os'),
    
    
]