from django.shortcuts import render, redirect
from .models import Produto
from pecas.models import Peca
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required
from .models import Produto
from pecas.models import ProdutoPeca




@login_required(login_url='logar')
def consulta_total(request):
    if request.method == "GET":
        return render(request, 'consulta_total.html')

    elif request.method == "POST":
        ptn = request.POST.get('ptn').upper()

        try:
            # Obtendo o produto pela PTN
            produto = Produto.objects.get(ptn=ptn)

            # Obtendo as peças associadas ao produto através do modelo intermediário ProdutoPeca
            produto_pecas = ProdutoPeca.objects.filter(produto=produto).select_related('peca')

            pecas = []
            for produto_peca in produto_pecas:
                # Adicionando informações da peça, incluindo o número do pedido e outras propriedades de ProdutoPeca
                pecas.append({
                    'peca': produto_peca.peca,  # Informações da peça
                    'defeito_peca_display': produto_peca.get_defeito_peca_display(),  # Rótulo do defeito
                    'tipo_peca_display': produto_peca.get_tipo_peca_display(),  # Rótulo do tipo de peça
                    'numero_pedido': produto_peca.numero_pedido,  # Número do pedido
                    'status': produto_peca.get_status_display(),  # Status da peça
                    'produto_peca_id': produto_peca.id,  # ID da relação ProdutoPeca
                })

            # Passando o produto e as peças para o template
            return render(request, 'consulta_total.html', {'produto': produto, 'pecas': pecas})

        except Produto.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Produto não encontrado')
            return redirect('consulta_total')
        
@login_required(login_url='logar')
def consulta_serie(request):
    if request.method == "GET":
        return render(request, 'consulta_serie.html')

    elif request.method == "POST":
        serie = request.POST.get('serie').upper()
        try:    
            produtos = Produto.objects.filter(serie=serie)
            
            if not produtos.exists():
                messages.add_message(request, constants.ERROR, 'Produto não encontrado')
                return redirect('consulta_serie')

            return render(request, 'consulta_serie.html', {'produtos': produtos})

        except Exception as e:
            messages.add_message(request, constants.ERROR, f'Ocorreu um erro: {str(e)}')
            return redirect('consulta_serie') 
              
@login_required(login_url='logar')        
def home(request):
    produtos_entrada = Produto.objects.filter(status="ENTRADA")
    produtos_triagem = Produto.objects.filter(status="TRIAGEM")
    produtos_conserto = Produto.objects.filter(status="CONSERTO")

    return render(request, 'home.html', {
        'produtos_entrada': produtos_entrada, 
        'produtos_triagem': produtos_triagem, 
        'produtos_conserto': produtos_conserto
    })