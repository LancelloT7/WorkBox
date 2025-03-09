from django.shortcuts import render, redirect, get_object_or_404
from pecas.models import Peca
from sku.models import Sku, Sufixo
from django.contrib import messages
from django.contrib.messages import constants
from django.http import JsonResponse, HttpResponse
from produto.models import Produto


# Create your views here.


def verificar_sku(request):
    if request.method == 'POST':
        sku_digitado = request.POST.get('sku')

        # Verificar se o SKU existe
        if sku_digitado is not None:
            try:
                sku_instance = Sku.objects.get(sku=sku_digitado)
                return redirect('cadastrar_peca', sku=sku_instance.sku)
            except Sku.DoesNotExist:
                messages.error(request, "SKU não encontrado.")
                return redirect('verificar_sku')

    return render(request, 'verificar_sku.html')

# Página 2: Formulário para Cadastrar a Peça
def cadastrar_pecas(request, sku):
    try:
        sku_instance = Sku.objects.get(sku=sku)
    except Sku.DoesNotExist:
        return HttpResponse("SKU não encontrado", status=404)

    if request.method == 'POST':
        sufixo = request.POST.get('sufixo')
        part_number = request.POST.get('part_number').upper()
        
        descricao = request.POST.get('descricao')
        observacao = request.POST.get('observacao')
        posicao = request.POST.get('posicao')
        defeito_pecas = request.POST.get('defeito_pecas')
        # Verifica se o sufixo pertence ao SKU
        try:
            sufixo_instance = Sufixo.objects.get(sufixo=sufixo, sku=sku_instance)
        except Sufixo.DoesNotExist:
            messages.error(request, 'Sufixo não encontrado para o SKU.')
            return redirect('cadastrar_pecas', sku=sku_instance.sku)
        
        

        if Peca.objects.filter(part_number=part_number).exists():
            messages.add_message(request, constants.ERROR, 'Já existe uma peça com esse part number')  
        else:             
            peca = Peca(
                sku=sku_instance,
                sufixo=sufixo_instance,
                part_number=part_number,
                descricao=descricao,
                posicao=posicao,
                observacao=observacao,
                defeito_pecas=defeito_pecas
            )
            peca.save() 

        messages.success(request, 'Peça cadastrada com sucesso.')
          # Ou redirecionar para outra página

    # Buscar os sufixos relacionados ao SKU
    sufixos = Sufixo.objects.filter(sku=sku_instance)

    return render(request, 'cadastrar_pecas.html', {
        'sku': sku_instance.sku,
        'sufixos': sufixos,
    })


def buscar_produto(request):
    if request.method == "GET":
        return render(request, "buscar_produto.html")

    elif request.method == "POST":
        procura = request.POST.get("procura", "").strip()
        if procura:
            produto = Produto.objects.filter(ptn__icontains=procura).first()
            if produto:
                pecas = Peca.objects.filter(sufixo=produto.sufixo)  # Filtra peças compatíveis pelo sufixo
                return render(request, "buscar_produto.html", {"produto": produto, "pecas": pecas})

        return render(request, "buscar_produto.html", {"erro": "Produto não encontrado!"})


def adicionar_pecas(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == "POST":
        # Atualiza o status do produto
        produto.status = "VERIFICAR DISPONIBILIDADE"
        produto.save()

        # Obtém as peças selecionadas no formulário
        pecas_selecionadas = request.POST.getlist("pecas")
        pecas = Peca.objects.filter(id__in=pecas_selecionadas)

        # Remove as peças que não estão mais selecionadas
        produto.peca.remove(*produto.peca.exclude(id__in=pecas_selecionadas))
        
        # Adiciona as novas peças ao produto
        produto.peca.add(*pecas)

        # Atualiza o defeito de cada peça
        for peca in pecas:
            defeito = request.POST.get(f"defeito_pecas_{peca.id}")
            if defeito:
                peca.defeito_pecas = defeito  # Atualiza o defeito da peça
                peca.save()  # Salva a peça com o novo defeito

        # Atualiza o status do produto se não houver peças associadas
        if not produto.peca.exists():
            produto.status = "LIBERADO PARA CONSERTO"
        produto.save()

        return redirect("buscar_produto")  # Redireciona para a busca após salvar

    return redirect("buscar_produto")
