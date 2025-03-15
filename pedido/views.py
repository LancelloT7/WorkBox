from django.shortcuts import render, redirect, get_object_or_404
from produto.models import Produto
from pecas.models import Peca
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required

# Create your views here

def consulta_pedido(request):
    if request.method == "GET":
        return render(request, 'consulta_pedido.html')

    elif request.method == "POST":
        ptn = request.POST.get('procura').upper()

        try:
            produto = Produto.objects.get(ptn=ptn)  # Buscando o produto pelo PTN
            pecas = produto.peca.all()  # Obtendo as peças específicas associadas ao produto

            # Adiciona os rótulos dos campos de escolha para cada peça
            for peca in pecas:
                peca.defeito_pecas_display = peca.get_defeito_pecas_display()
                peca.tipo_peca_display = peca.get_tipo_peca_display()

            return render(request, 'consulta_pedido.html', {'produto': produto, 'pecas': pecas})

        except Produto.DoesNotExist:
            messages.add_message(request, constants.ERROR, 'Produto não encontrado')
            return redirect('consulta_pedido')  # Redireciona para limpar o form
        
def salvar_codigos_pedido(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    pecas = produto.peca.all()    
    status_atualizado = False  # Flag para verificar se alguma peça foi alterada

    for peca in pecas:
        numero_pedido = request.POST.get(f'numero_pedido_{peca.id}')

        if numero_pedido:
            numero_pedido = numero_pedido.upper()  # Garante que o código seja salvo em maiúsculas
            peca.numero_pedido = numero_pedido
            peca.status = 'AGUARDANDO PEÇA'
            peca.save()
            status_atualizado = True  # Marca que pelo menos uma peça foi alterada
    # Atualiza o status do produto apenas se alguma peça tiver sido alterada
    if status_atualizado:
        produto.status = 'AGUARDANDO PEÇA'
        produto.save()

    messages.add_message(request, constants.SUCCESS, 'Número de pedido adicionado com sucesso!')
    return redirect('consulta_pedido')