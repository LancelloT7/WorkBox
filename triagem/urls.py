from django.urls import path
from . import views

urlpatterns = [

    path('cadastrar_triagem/', views.cad_triagem, name='cad_triagem'),
    path('buscar/', views.buscar, name='buscar'),
    path('form_triagem/', views.form_triagem, name='form_triagem'),


]