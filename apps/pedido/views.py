from django.shortcuts import render, redirect, get_object_or_404
from produto.models import Produto
from pecas.models import Peca, ProdutoPeca
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required

# Create your views here
@login_required(login_url='logar')
def consulta_pedido(request):
    if request.method == 'POST':
        # Procura o produto com base no PTN (part_number)
        ptn = request.POST.get('procura', None)
        if ptn:
            try:
                produto = Produto.objects.get(ptn=ptn)
                pecas = ProdutoPeca.objects.filter(produto=produto)
            except Produto.DoesNotExist:
                produto = None
                pecas = None
        else:
            produto = None
            pecas = None
    else:
        produto = None
        pecas = None

    return render(request, 'consulta_pedido.html', {'produto': produto, 'pecas': pecas})

@login_required(login_url='logar')
def salvar_codigos_pedido(request, produto_id):
    # Obtém o produto pelo ID ou retorna 404 se não existir
    produto = get_object_or_404(Produto, id=produto_id)
    
    # Obtém todas as peças associadas ao produto
    pecas = ProdutoPeca.objects.filter(produto=produto).select_related('peca')
    
    # Verifica se a requisição é POST
    if request.method == 'POST':
        # Flag para verificar se pelo menos uma peça tem um número de pedido
        tem_pedido = False
        
        # Itera sobre as peças para atualizar o número de pedido e o status
        for item in pecas:
            # Gera o nome do campo para o número do pedido
            numero_pedido_key = f'numero_pedido_{item.id}'
            
            # Obtém o valor enviado para o campo
            numero_pedido = request.POST.get(numero_pedido_key, None)
            
            # Verifica se o número do pedido foi fornecido
            if numero_pedido:
                numero_pedido = numero_pedido.upper()  # Converte para maiúsculas
                tem_pedido = True  # Indica que pelo menos uma peça tem um pedido
                
                # Verifica se o número do pedido contém "OK"
                if "OK" in numero_pedido:
                    item.status = "LIBERADO PARA CONSERTO"
                else:
                    item.status = "AGUARDANDO PEÇA"
                
                # Atualiza o número do pedido
                item.numero_pedido = numero_pedido
            else:
                # Se não houver número de pedido, define o status como "VERIFICAR DISPONIBILIDADE"
                item.status = "VERIFICAR DISPONIBILIDADE"
                item.numero_pedido = None
            
            # Salva as alterações na peça
            item.save()
        
        # Verifica o status das peças após atualizar todas
        status_pecas = [item.status for item in pecas]
        
        # Define o status do produto com base nas regras fornecidas
        if not tem_pedido:
            # Se nenhuma peça tiver pedido, o status do produto e das peças é "VERIFICAR DISPONIBILIDADE"
            produto.status = "VERIFICAR DISPONIBILIDADE"
        elif all(status == "LIBERADO PARA CONSERTO" for status in status_pecas):
            # Se todas as peças estiverem "LIBERADO PARA CONSERTO", o produto também estará
            produto.status = "LIBERADO PARA CONSERTO"
        elif all(status == "AGUARDANDO PEÇA" for status in status_pecas):
            # Se todas as peças estiverem "AGUARDANDO PEÇA", o produto também estará
            produto.status = "AGUARDANDO PEÇA"
        elif "AGUARDANDO PEÇA" in status_pecas and "LIBERADO PARA CONSERTO" in status_pecas:
            # Se houver uma mistura de "AGUARDANDO PEÇA" e "LIBERADO PARA CONSERTO", o produto estará "PEDIDO ATENDIDO PARCIALMENTE"
            produto.status = "PEDIDO ATENDIDO PARCIALMENTE"
        else:
            # Caso padrão (não deve ocorrer, mas é uma segurança)
            produto.status = "VERIFICAR DISPONIBILIDADE"
        
        # Salva o status atualizado do produto
        produto.save()
        
        # Redireciona para a página de consulta após salvar
        return redirect('consulta_pedido')
    
    # Se não for POST, renderiza o template com os dados do produto e peças
    return render(request, 'consulta_pedido.html', {
        'produto': produto,
        'pecas': pecas,
    })