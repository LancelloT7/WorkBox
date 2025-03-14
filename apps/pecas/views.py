from django.shortcuts import render, redirect, get_object_or_404
from pecas.models import Peca, ProdutoPeca
from sku.models import Sku, Sufixo
from django.contrib import messages
from django.contrib.messages import constants
from django.http import JsonResponse, HttpResponse
from produto.models import Produto
from django.contrib.auth.decorators import login_required

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
        
        descricao = request.POST.get('descricao').upper()
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
                # Obtendo todas as peças associadas ao produto
                produto_pecas = ProdutoPeca.objects.filter(produto=produto)

                # Recuperando as peças relacionadas e associando as informações de tipo e defeito
                pecas = []
                for produto_peca in produto_pecas:
                    peca = produto_peca.peca
                    peca.tipo_peca = produto_peca.tipo_peca
                    peca.defeito_pecas = produto_peca.defeito_pecas
                    pecas.append(peca)

                # Extrai as escolhas de tipo de peça e defeito
                tipo_peca_choices = Peca.TIPO_PECA
                defeito_pecas_choices = Peca.DEFEITO_PECAS

                return render(request, "buscar_produto.html", {
                    "produto": produto,
                    "pecas": pecas,
                    "tipo_peca_choices": tipo_peca_choices,
                    "defeito_pecas_choices": defeito_pecas_choices,
                })

        return render(request, "buscar_produto.html", {"erro": "Produto não encontrado!"})

def adicionar_pecas(request, produto_id=None):
    erro = None
    produto = None
    pecas = Peca.objects.all()  # Você pode filtrar as peças conforme necessário

    if request.method == 'POST':

        # Verificando se estamos buscando um produto pelo PTN
        if 'procura' in request.POST:
            ptn = request.POST['procura']
            try:
                produto = Produto.objects.get(ptn=ptn)
                
            except Produto.DoesNotExist:
                erro = "Produto não encontrado. Verifique o PTN."
        
        # Verificando se estamos associando peças a um produto
        elif 'pecas' in request.POST and produto_id:
            
            produto = get_object_or_404(Produto, id=produto_id)
            pecas_selecionadas = request.POST.getlist('pecas')  # Obtendo as peças selecionadas

            for peca_id in pecas_selecionadas:
                peca = get_object_or_404(Peca, id=peca_id)  # Obtenha a peça com base no ID
                tipo_peca = request.POST.get(f'tipo_peca_{peca_id}')  # Obtendo tipo da peça
                defeito_peca = request.POST.get(f'defeito_pecas_{peca_id}')  # Obtendo defeito da peça

                # Criando a associação ProdutoPeca
                ProdutoPeca.objects.create(
                    produto=produto,
                    peca=peca,
                    status=peca.status,  # Usando o status da peça
                    tipo_peca=tipo_peca,  # Adicionando o tipo de peça
                    defeito_peca=defeito_peca,  # Adicionando o defeito da peça
                )                
                # Mensagem de sucesso
                messages.success(request, "Peça adicionada ao produto com sucesso!")
            # Redirecionando para a página de adicionar peças com o produto já associado
            return redirect('adicionar_pecas', produto_id=produto.id)

    return render(request, 'buscar_produto.html', {
        'produto': produto,
        'erro': erro,
        'pecas': pecas,
    })

    
    
