from django.shortcuts import render, get_object_or_404
from produto.models import Produto
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required
from funcionario.models import Funcionario


# Create your views here.

@login_required(login_url='logar')
def embalagem(request):
    funcionarios = Funcionario.objects.all()
    if request.method == "GET":
        return render(request, 'embalagem.html', {'funcionarios': funcionarios})

    elif request.method == "POST":
        ptns = request.POST.getlist('ptn')
        funcionario_id = request.POST.get('funcionario_id')
        funcionario = get_object_or_404(Funcionario, id=funcionario_id)

        # Filtra todos os produtos correspondentes aos PTNs informados
        produtos = Produto.objects.filter(ptn__in=ptns)


        if not produtos.exists():
            messages.error(request, "Nenhum produto encontrado para os PTNs informados.")
            return render(request, 'embalagem.html')

        # Atualiza os produtos encontrados
        for produto in produtos:
            produto.responsavel_embalagem = funcionario
            produto.status = 'EMBALADO'
            produto.save()
            
        messages.add_message(request, constants.SUCCESS, "Produtos atualizados com sucesso!")

        # Retorna a lista de produtos atualizados para o template
        return render(request, 'embalagem.html', {'produtos': produtos})



