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
    produto = Produto.objects.get(id=produto_id)
    pecas = ProdutoPeca.objects.filter(produto=produto)

    # Verificando se a requisição é POST
    if request.method == 'POST':
        # Iterando sobre as peças para atualizar o número de pedido na tabela intermediária
        for item in pecas:
            print(f"ID da Peça: {item.id} | Descrição: {item.peca.descricao}")
            numero_pedido_key = f'numero_pedido_{item.id}'  # Identificando o campo correto de número de pedido
            
            # Verificando o que está sendo enviado no request
            print(f"Chave: {numero_pedido_key} | Valor recebido: {request.POST.get(numero_pedido_key)}")
            
            numero_pedido = request.POST.get(numero_pedido_key, None)

            # Verificando se existe o número de pedido e se é diferente do que já está registrado
            if numero_pedido and numero_pedido != item.numero_pedido:
                print(f"Atualizando número do pedido para a peça {item.id}: {numero_pedido}")
                item.numero_pedido = numero_pedido  # Atualizando na tabela intermediária ProdutoPeca
                item.save()  # Salvando a alteração

    # Após salvar, redireciona de volta para a página de consulta
    return redirect('consulta_pedido')


@login_required(login_url='logar')
def salvar_codigos_pedido(request, produto_id):
    # Obtém o produto pelo ID ou retorna 404 se não existir
    produto = get_object_or_404(Produto, id=produto_id)
    
    # Obtém todas as peças associadas ao produto
    pecas = ProdutoPeca.objects.filter(produto=produto).select_related('peca')
    
    # Verifica se a requisição é POST
    if request.method == 'POST':
        # Itera sobre as peças para atualizar o número de pedido
        for item in pecas:
            # Gera o nome do campo para o número do pedido
            numero_pedido_key = f'numero_pedido_{item.id}'
            
            # Obtém o valor enviado para o campo
            numero_pedido = request.POST.get(numero_pedido_key, None)
            
            # Atualiza o status para "AGUARDANDO PEÇA"
            item.status = "AGUARDANDO PEÇA"
            
            # Verifica se o número do pedido foi alterado
            if numero_pedido and numero_pedido != item.numero_pedido:
                item.numero_pedido = numero_pedido
                item.save()  # Salva a alteração
        
        # Redireciona para a página de consulta após salvar
        return redirect('consulta_pedido')
    
    # Se não for POST, renderiza o template com os dados do produto e peças
    return render(request, 'consulta_pedido.html', {
        'produto': produto,
        'pecas': pecas,
    })


