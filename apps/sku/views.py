from django.shortcuts import render, redirect
from .models import Sku, Sufixo
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.

def cad_sku(request):

    if request.method == "GET":
        return render(request, 'cad_sku.html')

    elif request.method == "POST":

        sku = request.POST.get('sku')
        modelo = request.POST.get('modelo')

        if Sku.objects.filter(sku=sku).exists() :
            
            messages.add_message(request, constants.ERROR, 'SKU já existe')
            return redirect('cad_sku')
        
        else:
            novo_sku = Sku.objects.create(sku=sku, modelo=modelo)

        messages.add_message(request, constants.SUCCESS, 'SKU Cadastrado')
        return redirect('cad_sku')

def cad_sufixo(request):

    if request.method == "GET":
        return render(request, 'cad_sufixo.html')

    elif request.method == "POST":
        
        sku = request.POST.get('sku')
        sufixo = request.POST.get('sufixo')

        try:
            sku_instace = Sku.objects.get(sku=sku)

            if sku:

                if Sufixo.objects.filter(sufixo=sufixo).exists():

                    messages.add_message(request, constants.ERROR, 'Sufixo já existe')
                    return redirect('cad_sufixo')
                else:
                    sufixo = Sufixo.objects.create(sku=sku_instace, sufixo=sufixo)

                    messages.add_message(request, constants.SUCCESS, 'Cadastrato realizado com sucesso')
                    return redirect('cad_sufixo')
        except:
            messages.add_message(request, constants.ERROR, 'SKU não encontrado no banco de dados')
            return redirect('cad_sufixo')    





           