from django.urls import path
from . import views

urlpatterns = [

    path('inserir_conserto/', views.conserto, name='conserto'),
    
]