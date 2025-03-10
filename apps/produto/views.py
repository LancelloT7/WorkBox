from django.shortcuts import render, redirect
from .models import Produto
from pecas.models import Peca
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.

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

        
    
def home(request):
    return render(request, 'home.html')        