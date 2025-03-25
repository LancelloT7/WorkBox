from django.urls import path
from . import views

urlpatterns = [

    path('encerrar/', views.encerrar, name='encerrar'),
    
]