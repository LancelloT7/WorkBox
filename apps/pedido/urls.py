from django.urls import path
from . import views

urlpatterns = [

    path('consulta_pedido/', views.consulta_pedido, name='consulta_pedido'),
    path('salvar_codigos_pedido/<int:produto_id>/', views.salvar_codigos_pedido, name='salvar_codigos_pedido'),
    
]