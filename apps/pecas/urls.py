from django.urls import path
from . import views

urlpatterns = [

    path('cadastrar_peca/<str:sku>/', views.cadastrar_pecas, name='cadastrar_peca'),
    path('verificar_sku/', views.verificar_sku, name='verificar_sku'),
    
]