from django.urls import path
from . import views

urlpatterns = [

    path('consulta_total/', views.consulta_total, name='consulta_total'),
    path('consulta_serie/', views.consulta_serie, name='consulta_serie'),
    path('inicio/', views.home, name="home"),
    
]