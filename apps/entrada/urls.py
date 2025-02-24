from django.urls import path
from . import views

urlpatterns = [

    path('cadastrar_produtos/', views.entrada, name='entrada'),
    path('get-sku-data/', views.get_sku_data, name='get_sku_data'),
    
]