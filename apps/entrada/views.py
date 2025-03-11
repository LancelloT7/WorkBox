from django.shortcuts import render, redirect
from .models import Entrada
from produto.models import Produto
from django.contrib import messages
from django.contrib.messages import constants
from sku.models import Sku, Sufixo
from funcionario.models import Funcionario
from django.http import JsonResponse
from datetime import datetime


# Create your views here.
def sku_form_view(request):
    return render(request, "sku_form.html")

def get_sku_data(request):
    sku = request.GET.get("sku")
    
    if not sku:
        return JsonResponse({"error": "SKU não fornecido"}, status=400)

    try:
        produto = Produto.objects.get(sku=sku)  # Verifica se o SKU existe no banco
        sufixos = list(produto.sufixos.values_list("id", "descricao"))  # Pegando os sufixos
        
        return JsonResponse({"modelo": produto.modelo, "sufixos": sufixos})
    
    except Produto.DoesNotExist:
        return JsonResponse({"error": "SKU não encontrado"}, status=404)


def entrada(request):
    all_funcionarios = Funcionario.objects.all()
    all_produtos  = Produto.objects.all()
    data_atual = datetime.today().date()
    produtos_hoje = Produto.objects.filter(data_entrada__date=data_atual)
    

    if request.method == "GET":
        return render(request, 'entrada.html', {'produtos_hoje':produtos_hoje, 'produtos': all_produtos,'funcionarios': all_funcionarios, 'defeito_choices': Produto.DEFEITO_CHOICES})

    elif request.method == "POST":
        ptn = request.POST.get('ptn', '').upper()
        serie = request.POST.get('serie', '').upper()
        sku_id = request.POST.get('sku')
        sufixo_id = request.POST.get('sufixo')
        responsavel_entrada_id = request.POST.get('responsavel_entrada')
        defeito = request.POST.get('defeito')
        observacao = request.POST.get('observacao')

        # Validação do SKU
        try:
            sku = Sku.objects.get(sku=sku_id)
        except Sku.DoesNotExist:
            messages.error(request, 'SKU inválido.')
            return redirect('entrada')

        # Verifica se o Produto já existe
        contador = 0
        novo_ptn = ptn  # Começa com o PTN original
        
        if Produto.objects.filter(ptn=ptn).exists():
            produto = Produto.objects.get(ptn=ptn)
            if produto.serie !=serie:
                messages.success(request, 'Produto tem uma provavel etiqueta duplicada favor verificar.')
                return redirect('entrada')
        
            
        while Produto.objects.filter(ptn=novo_ptn, serie=serie).exists():
                
            contador += 1  # Incrementa para a próxima verificação
            novo_ptn = f"{ptn}-{contador}"  # Adiciona o contador ao PTN
                

        ptn = novo_ptn  # Atualiza o PTN final antes de salvar
        # Obtém os objetos do banco
        sufixo = Sufixo.objects.get(id=sufixo_id, sku=sku) if sufixo_id else None
        try:
            responsavel_entrada = Funcionario.objects.get(id=responsavel_entrada_id)
        except Funcionario.DoesNotExist:
            print(f"ID do responsável recebido: {responsavel_entrada_id}")
            messages.add_message(request, constants.ERROR, 'Funcionário inválido.')
            return redirect('entrada')

            # Criação do Produto
        produto = Produto(
            ptn=ptn,
            serie=serie,
            sku=sku,
            sufixo=sufixo,
            modelo=sku,  # O modelo já está na classe Sku
            responsavel_entrada=responsavel_entrada,
            defeito=defeito,
            observacao=observacao
        )
        if  produto.defeito == "Venda Direta":
            produto.defeito_especifico = "Tela Quebrada"
        try:
            produto.save()
        except:
            messages.add_message(request, constants.ERROR, 'Não foi possivel cadastrar o produto.')  
                  
    messages.success(request, 'Produto cadastrado com sucesso.')
    return redirect('entrada')

def get_sku_data(request):
    """ Retorna os dados do SKU para preenchimento automático """
    sku_value = request.GET.get("sku", None)
    if sku_value:
        try:
            sku = Sku.objects.get(sku=sku_value)
            sufixos = Sufixo.objects.filter(sku=sku).values_list("id", "sufixo")
            return JsonResponse({"modelo": sku.modelo, "sufixos": list(sufixos)})
        except Sku.DoesNotExist:
            return JsonResponse({"error": "SKU não encontrado"}, status=404)
    return JsonResponse({"error": "Nenhum SKU fornecido"}, status=400)





