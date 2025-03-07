from django.urls import path
from . import views

urlpatterns = [

    path('cadastrar_peca/<str:sku>/', views.cadastrar_pecas, name='cadastrar_peca'),
    path('verificar_sku/', views.verificar_sku, name='verificar_sku'),
    path("buscar/", views.buscar_produto, name="buscar_produto"),
    path("adicionar-pecas/<int:produto_id>/", views.adicionar_pecas, name="adicionar_pecas"),
    
]