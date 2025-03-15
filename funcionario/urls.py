from django.urls import path
from . import views

urlpatterns = [

    path('cadastrar_funcionario/', views.cad_funcionario, name='cad_funcionario'),
    
]