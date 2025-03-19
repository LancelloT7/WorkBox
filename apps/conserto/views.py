from django.shortcuts import render, get_object_or_404
from produto.models import Produto
from pecas.models import ProdutoPeca
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required


# Create your views here.


def conserto(request):
    if request.method == "GET":
        return render(request, 'conserto.html')

    elif request.method == "POST":
        ptns = request.POST.getlist('ptn')

        # Filtra todos os produtos correspondentes aos PTNs informados
        produtos = Produto.objects.filter(ptn__in=ptns)


        if not produtos.exists():
            messages.error(request, "Nenhum produto encontrado para os PTNs informados.")
            return render(request, 'conserto.html')

        # Atualiza os produtos encontrados
        for produto in produtos:
            produto.observacao = "Troca de Peça"
            produto.status = 'EMBALAGEM'
            produto.save()

        messages.add_message(request, constants.SUCCESS, "Produtos atualizados com sucesso!")

        # Retorna a lista de produtos atualizados para o template
        return render(request, 'conserto.html', {'produtos': produtos})



