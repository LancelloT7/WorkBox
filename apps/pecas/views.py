from django.shortcuts import render, redirect
from pecas.models import Peca
from sku.models import Sku, Sufixo
from django.contrib import messages
from django.contrib.messages import constants
from django.http import JsonResponse, HttpResponse


# Create your views here.


def verificar_sku(request):
    if request.method == 'POST':
        sku_digitado = request.POST.get('sku')

        # Verificar se o SKU existe
        if sku_digitado is not None:
            try:
                sku_instance = Sku.objects.get(sku=sku_digitado)
                return redirect('cadastrar_peca', sku=sku_instance.sku)
            except Sku.DoesNotExist:
                messages.error(request, "SKU não encontrado.")
                return redirect('verificar_sku')

    return render(request, 'verificar_sku.html')

# Página 2: Formulário para Cadastrar a Peça
def cadastrar_pecas(request, sku):
    try:
        sku_instance = Sku.objects.get(sku=sku)
    except Sku.DoesNotExist:
        return HttpResponse("SKU não encontrado", status=404)

    if request.method == 'POST':
        sufixo = request.POST.get('sufixo')
        part_number = request.POST.get('part_number').upper()
        
        descricao = request.POST.get('descricao')
        observacao = request.POST.get('observacao')

        # Verifica se o sufixo pertence ao SKU
        try:
            sufixo_instance = Sufixo.objects.get(sufixo=sufixo, sku=sku_instance)
        except Sufixo.DoesNotExist:
            messages.error(request, 'Sufixo não encontrado para o SKU.')
            return redirect('cadastrar_pecas', sku=sku_instance.sku)

        if Peca.objects.filter(part_number=part_number).exists():
            messages.add_message(request, constants.ERROR, 'Já existe uma peça com esse part number')  
        else:             
            peca = Peca(
                sku=sku_instance,
                sufixo=sufixo_instance,
                part_number=part_number,
                descricao=descricao,
                observacao=observacao
            )
            peca.save() 

        messages.success(request, 'Peça cadastrada com sucesso.')
          # Ou redirecionar para outra página

    # Buscar os sufixos relacionados ao SKU
    sufixos = Sufixo.objects.filter(sku=sku_instance)

    return render(request, 'cadastrar_pecas.html', {
        'sku': sku_instance.sku,
        'sufixos': sufixos,
    })