from django.shortcuts import render, redirect
from .models import Sku, Sufixo
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='logar')
def cad_sku_sufixo(request):
    sku_instance = None
    sufixos = []

    if request.method == 'GET':
        return render(request, 'cad_sku.html')

    elif request.method == 'POST':
        # Obtém o SKU informado pelo usuário e remove espaços extras
        sku_input = request.POST.get('sku', '').strip()

        if not sku_input:
            messages.error(request, 'O campo SKU é obrigatório!')
            return render(request, 'cad_sku.html')

        try:
                        # Verifica se o SKU já existe, considerando possíveis variações de maiúsculas/minúsculas
            sku_instance = Sku.objects.get(sku=sku_input)

            # Se o SKU for encontrado, busca os sufixos relacionados a ele
            sufixos = sku_instance.sku_sufixo.all()

            # Verifica se foi enviado um novo sufixo para adicionar ao SKU
            sufixo_input = request.POST.get('sufixo', '').strip()
            if sufixo_input:
                novo_sufixo = Sufixo(sku=sku_instance, sufixo=sufixo_input)
                novo_sufixo.save()
                messages.success(request, 'Novo sufixo cadastrado com sucesso!')
                return redirect('cad_sku_sufixo')  # Redireciona para evitar duplicação do formulário
            else:
                messages.error(request, 'O campo Sufixo é obrigatório!')

        except Sku.DoesNotExist:
            # Se o SKU não existe, cadastrar um novo SKU com modelo e sufixo inicial
            modelo_input = request.POST.get('modelo', '').strip().upper()
            sufixo_input = request.POST.get('sufixo', '').strip().upper()

            if sku_input and modelo_input and sufixo_input:
                # Cria o novo SKU
                novo_sku = Sku(sku=sku_input, modelo=modelo_input)
                novo_sku.save()

                # Cria o sufixo relacionado ao novo SKU
                novo_sufixo = Sufixo(sku=novo_sku, sufixo=sufixo_input)
                novo_sufixo.save()

                messages.success(request, 'SKU, modelo e sufixo cadastrados com sucesso!')
                return redirect('cad_sku_sufixo')  # Redireciona após o cadastro para evitar duplicação

            else:
                messages.error(request, 'Todos os campos (SKU, modelo e sufixo) são obrigatórios para cadastrar um novo SKU.')

        return render(request, 'cad_sku.html', {
            'sku_instance': sku_instance,
            'sufixos': sufixos,
        })
