from django.urls import path
from . import views

urlpatterns = [

    path('produtos_embalados/', views.embalagem, name='embalagem'),
]