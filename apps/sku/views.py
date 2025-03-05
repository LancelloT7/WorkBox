from django.shortcuts import render, redirect
from .models import Sku, Sufixo
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.



def cad_sku_sufixo(request):
    sku_instance = None
    sufixos = []
    if request.method == 'GET':
        
        return render(request, 'cad_sku.html')

    elif request.method == 'POST':
        sku_input = request.POST.get('sku').strip()

        try:
            # Verifica se o SKU já existe
            sku_instance = Sku.objects.get(sku=sku_input)
            sufixos = sku_instance.sku_sufixo.all()  # Busca os sufixos relacionados ao SKU

            # Se for enviado um novo sufixo, adiciona ao SKU existente
            if 'sufixo' in request.POST:
                sufixo_input = request.POST.get('sufixo').strip()
                novo_sufixo = Sufixo(sku=sku_instance, sufixo=sufixo_input)
                novo_sufixo.save()
                messages.success(request, 'Novo sufixo cadastrado com sucesso!')
                return redirect('cad_sku_sufixo')

        except Sku.DoesNotExist:
            # Se o SKU não existe, cadastrar um novo SKU com modelo e sufixo inicial
            modelo_input = request.POST.get('modelo').strip()
            sufixo_input = request.POST.get('sufixo').strip()

            novo_sku = Sku(sku=sku_input, modelo=modelo_input)
            novo_sku.save()

            novo_sufixo = Sufixo(sku=novo_sku, sufixo=sufixo_input)
            novo_sufixo.save()

            messages.success(request, 'SKU, modelo e sufixo cadastrados com sucesso!')
            return render(request, 'cad_sku.html')

    return render(request, 'cad_sku.html', {
        'sku_instance': sku_instance,
        'sufixos': sufixos,
    })