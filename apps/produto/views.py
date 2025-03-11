from django.shortcuts import render, redirect
from .models import Produto
from pecas.models import Peca
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='logar')
def consulta_total(request):
    if request.method == "GET":
        return render(request, 'consulta_total.html')

    elif request.method == "POST":
        ptn = request.POST.get('ptn').upper()

        try:
            produto = Produto.objects.get(ptn=ptn)
            pecas = produto.peca.all()  # Obtendo todas as peças relacionadas ao produto

            # Adiciona os rótulos dos campos de escolha
            for peca in pecas:
                peca.defeito_pecas_display = peca.get_defeito_pecas_display()
                peca.tipo_peca_display = peca.get_tipo_peca_display()

            return render(request, 'consulta_total.html', {'produto': produto, 'pecas': pecas})
        except Produto.DoesNotExist:
            messages.add_message(request, constants.ERROR, 'Produto não encontrado')
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

            pecas = []
            for produto in produtos:
                pecas.extend(produto.peca.all())  # Pegando todas as peças de cada produto

            # Adiciona os rótulos dos campos de escolha
            for peca in pecas:
                produto.peca.defeito_pecas_display = peca.get_defeito_pecas_display()
                produto.peca.tipo_peca_display = peca.get_tipo_peca_display()

            return render(request, 'consulta_serie.html', {'produtos': produtos, 'pecas': pecas})

        except Exception as e:
            messages.add_message(request, constants.ERROR, f'Ocorreu um erro: {str(e)}')
            return redirect('consulta_serie')       

        
@login_required(login_url='logar') 
def home(request):
    return render(request, 'home.html')        