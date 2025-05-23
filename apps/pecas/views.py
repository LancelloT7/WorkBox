from django.shortcuts import render, redirect, get_object_or_404
from pecas.models import Peca, ProdutoPeca
from sku.models import Sku, Sufixo
from django.contrib import messages
from django.contrib.messages import constants
from django.http import JsonResponse, HttpResponse
from produto.models import Produto
from django.contrib.auth.decorators import login_required
from funcionario.models import Funcionario

# Procurar SKU para cadastrar uma nova peça
@login_required(login_url='logar')
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


@login_required(login_url='logar')
def cadastrar_pecas(request, sku):
    try:
        sku_instance = Sku.objects.get(sku=sku)
    except Sku.DoesNotExist:
        return HttpResponse("SKU não encontrado", status=404)

    if request.method == 'POST':
        sufixo = request.POST.get('sufixo')
        part_number = request.POST.get('part_number', '').upper()
        descricao = request.POST.get('descricao', '').upper()
        observacao = request.POST.get('observacao', '')
        posicao = request.POST.get('posicao', '')
        defeito_pecas = request.POST.get('defeito_pecas', '')


        # Verifica se o sufixo pertence ao SKU
        try:
            sufixo_instance = Sufixo.objects.get(sufixo=sufixo, sku=sku_instance)
        except Sufixo.DoesNotExist:
            messages.error(request, 'Sufixo não encontrado para o SKU.')
            return redirect('cadastrar_pecas', sku=sku_instance.sku)

        # Verifica se já existe uma peça com o mesmo part_number
        
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

    # Buscar os sufixos relacionados ao SKU
    sufixos = Sufixo.objects.filter(sku=sku_instance)

    return render(request, 'cadastrar_pecas.html', {
        'sku': sku_instance.sku,
        'sufixos': sufixos,
    })


# Buscar produto para adicionar peças
@login_required(login_url='logar')
def buscar_produto(request):
    funcionarios = Funcionario.objects.all()
    if request.method == "GET":
        return render(request, "buscar_produto.html", {'funcionarios':funcionarios})

    elif request.method == "POST":
        procura = request.POST.get("procura", "").strip().upper()

        if procura:
            produto = Produto.objects.filter(ptn__icontains=procura).first()
            if produto:
                pecas = Peca.objects.filter(sku=produto.sku, sufixo=produto.sufixo)
                
                if pecas.exists():
                   
                    tipo_peca_choices = Peca.TIPO_PECA
                    defeito_pecas_choices = Peca.DEFEITO_PECAS

                    return render(request, "buscar_produto.html", {
                        "produto": produto,
                        "pecas": pecas,
                        "tipo_peca_choices": tipo_peca_choices,
                        "defeito_pecas_choices": defeito_pecas_choices,
                        "funcionarios":funcionarios,
                    })
                else:
                    return render(request, "buscar_produto.html", {"erro": "Nenhuma peça encontrada para este produto!"})

            else:
                return render(request, "buscar_produto.html", {"erro": "Produto não encontrado!"})

        else:
            return render(request, "buscar_produto.html", {"erro": "Por favor, insira um PTN válido para a pesquisa."})

@login_required(login_url='logar')
def adicionar_pecas(request, produto_id=None):
    erro = None
    produto = None
    pecas = Peca.objects.all()  # Você pode filtrar as peças conforme necessário
    funcionarios = Funcionario.objects.all()  # Listando funcionários para escolher um responsável

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
            pecas_selecionadas = request.POST.getlist('pecas')
            funcionario_id = request.POST.get('funcionario')  # Obtendo o ID do responsável
            funcionario = get_object_or_404(Funcionario, id=funcionario_id)

            # Atualizando o responsável pelas peças no produto
            produto.responsavel_pecas = funcionario
            produto.save()

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

            # Verifica se o produto tem peças associadas
            if produto.produtopecas.exists():  # Verifica se há peças associadas ao produto
                produto.status = "VERIFICAR DISPONIBILIDADE"
            else:
                produto.status = "LIBERADO PARA CONSERTO"

            # Salva o status atualizado do produto
            produto.save()

            # Mensagem de sucesso
            messages.success(request, "Peça adicionada ao produto e responsável atualizado com sucesso!")
            # Redirecionando para a página de adicionar peças com o produto já associado
            return redirect('buscar_produto')

    return render(request, 'buscar_produto.html', {
        'produto': produto,
        'erro': erro,
        'pecas': pecas,
        'funcionarios': funcionarios,  # Enviando funcionários para o template
    })


    
    
