from django.shortcuts import render, get_object_or_404, redirect
from produto.models import Produto
from pecas.models import ProdutoPeca
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required
from funcionario.models import Funcionario


# Create your views here.


def conserto(request):
    funcionarios = Funcionario.objects.all()
    if request.method == "GET":
        return render(request, 'conserto.html',{'funcionarios': funcionarios})

    elif request.method == "POST":
        ptns = request.POST.getlist('ptn')
        funcionario_id = request.POST.get('funcionario')

        try:
            responsavel_conserto = Funcionario.objects.get(id=funcionario_id)
        except Funcionario.DoesNotExist:
            print(f"ID do responsável recebido: {funcionario_id}")
            messages.add_message(request, constants.ERROR, 'Funcionário inválido.')
            return redirect('conserto')
        
        # Filtra todos os produtos correspondentes aos PTNs informados
        produtos = Produto.objects.filter(ptn__in=ptns)


        if not produtos.exists():
            messages.error(request, "Nenhum produto encontrado para os PTNs informados.")
            return render(request, 'conserto.html')

        # Atualiza os produtos encontrados
        for produto in produtos:
            produto.responsavel_conserto = responsavel_conserto
            produto.observacao = "Troca de Peça"
            produto.status = 'EMBALAGEM'
            produto.save()

        messages.add_message(request, constants.SUCCESS, "Produtos atualizados com sucesso!")

        # Retorna a lista de produtos atualizados para o template
        return render(request, 'conserto.html', {'produtos': produtos})



