from django.urls import path
from . import views

urlpatterns = [

    path('consulta_total/', views.consulta_total, name='consulta_total'),
    path('inicio/', views.home, name="home"),
    
]