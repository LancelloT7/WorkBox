from django.shortcuts import render, redirect
from .models import Produto
from pecas.models import Peca
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required
from .models import Produto
from pecas.models import ProdutoPeca




def consulta_total(request):
    if request.method == "GET":
        return render(request, 'consulta_total.html')

    elif request.method == "POST":
        ptn = request.POST.get('ptn').upper()

        try:
            # Obtendo o produto pela PTN
            produto = Produto.objects.get(ptn=ptn)

            # Obtendo as peças associadas ao produto através do modelo intermediário ProdutoPeca
            produto_pecas = ProdutoPeca.objects.filter(produto=produto)

            pecas = []
            for produto_peca in produto_pecas:
                peca = produto_peca.peca
                # Adicionando rótulos de defeito e tipo
                pecas.append({
                    'peca': peca,
                    'defeito_peca_display': produto_peca.get_defeito_peca_display(),  # Correto
                    'tipo_peca_display': produto_peca.get_tipo_peca_display(),  # Correto
                })

            # Passando o produto e as peças para o template
            return render(request, 'consulta_total.html', {'produto': produto, 'pecas': pecas})

        except Produto.DoesNotExist:
            messages.add_message(request, constants.ERROR, 'Produto não encontrado')
            return redirect('consulta_total')

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

            pecas = []
            for produto in produtos:
                pecas.extend(produto.peca.all())  # Pegando todas as peças de cada produto

            # Adiciona os rótulos dos campos de escolha
            for peca in pecas:
                produto_peca = ProdutoPeca.objects.filter(produto=produto, peca=peca).first()
    
            if produto_peca:  # Verifica se existe um relacionamento ProdutoPeca
                defeito_pecas_display = produto_peca.get_defeito_pecas_display()
                tipo_peca_display = produto_peca.get_tipo_peca_display()

            return render(request, 'consulta_serie.html', {'produtos': produtos, 'pecas': pecas})

        except Exception as e:
            messages.add_message(request, constants.ERROR, f'Ocorreu um erro: {str(e)}')
            return redirect('consulta_serie')       
        
def home(request):
    return render(request, 'home.html')        