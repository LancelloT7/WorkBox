from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from produto.models import Produto
from pecas.models import ProdutoPeca  # Certifique-se de importar o modelo correto
import pandas as pd
from sku.models import Sufixo, Sku
from openpyxl import load_workbook

@login_required(login_url='logar')
def gerar_relatorio(request):
    if request.method == "GET":
        return render(request, 'relatorio.html')  # Página do formulário

    elif request.method == "POST":
        status_filtro = request.POST.get('status', '').strip()  # Obtém o status do formulário

        try:
            # Obtendo os produtos filtrados por status (se fornecido)
            produtos = Produto.objects.all()
            if status_filtro:
                produtos = produtos.filter(status=status_filtro)

            # Criando lista com os dados para o relatório
            dados_relatorio = []
            for produto in produtos:
                # Obtendo as peças associadas ao produto
                produto_pecas = ProdutoPeca.objects.filter(produto=produto).select_related('peca')

                for produto_peca in produto_pecas:
                    dados_relatorio.append({
                        'PTN': produto.ptn, 
                        'Serie': produto.serie, 
                        'Defeito': produto.defeito_especifico,
                        'Status do Produto': produto.status,   
                        'Data de Entrada': produto.data_entrada.strftime('%d/%m/%Y'),  

                        'Número do Pedido': produto_peca.numero_pedido,
                        'Nome da Peça': produto_peca.peca.descricao,  
                        'Defeito da Peça': produto_peca.get_defeito_peca_display(),
                        'Tipo da Peça': produto_peca.get_tipo_peca_display(),
                        'Status da Peça': produto_peca.get_status_display(),
                    })

            # Criando DataFrame com os dados coletados
            df = pd.DataFrame(dados_relatorio)

            # Gerando o arquivo Excel
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="relatorio_produtos_{status_filtro or 'todos'}.xlsx"'
            df.to_excel(response, index=False, engine='openpyxl')  # Gerando .xlsx com pandas

            return response

        except Exception as e:
            messages.error(request, f'Erro ao gerar relatório: {str(e)}')
            return redirect('relatorio')  # Redireciona para a página do formulário

@login_required(login_url='logar')
def gerar_os(request):
    try:
        # Filtrando os produtos que ainda não foram impressos
        produtos = Produto.objects.filter(impresso=False)

        # Lista para armazenar os dados para a Ordem de Serviço
        dados_os = []

        # Percorrendo os produtos para coletar as peças associadas
        for produto in produtos:
            # Obtendo o SKU, Modelo e Sufixo associados ao produto
            sku = produto.sku.sku if produto.sku else 'N/A'
            modelo = produto.sku.modelo if produto.sku else 'N/A'
            sufixo = produto.sku.sku_sufixo.first().sufixo if produto.sku and produto.sku.sku_sufixo.exists() else 'N/A'

            # Obtendo os responsáveis (Funcionario) para cada função
            responsavel_entrada = produto.responsavel_entrada.nome if produto.responsavel_entrada else 'N/A'
            responsavel_triagem = produto.responsavel_triagem.nome if produto.responsavel_triagem else 'N/A'
            responsavel_pecas = produto.responsavel_pecas.nome if produto.responsavel_pecas else 'N/A'

            # Obtendo as peças associadas ao produto
            produto_pecas = ProdutoPeca.objects.filter(produto=produto).select_related('peca')

            if produto_pecas.exists():
                for produto_peca in produto_pecas:
                    dados_os.append({
                        # Campos unificados
                        'PTN': produto.ptn,
                        'Série': produto.serie,
                        'Data de Entrada': produto.data_entrada.strftime('%d/%m/%Y'),
                        'Defeito Específico': produto.defeito_especifico,
                        'SKU': sku,
                        'Modelo': modelo,
                        'Sufixo': sufixo,

                        # Dados dos responsáveis
                        'Responsável Entrada': responsavel_entrada,
                        'Responsável Triagem': responsavel_triagem,
                        'Responsável Peças': responsavel_pecas,

                        # Dados das peças
                        'Número do Pedido': produto_peca.numero_pedido,
                        'Nome da Peça': produto_peca.peca.descricao,
                        'Defeito da Peça': produto_peca.get_defeito_peca_display(),
                        'Tipo da Peça': produto_peca.get_tipo_peca_display(),
                        'Status da Peça': produto_peca.get_status_display(),
                    })
            else:
                # Caso não tenha peças associadas, ainda assim geramos os dados do produto
                dados_os.append({
                    # Campos unificados
                    'PTN': produto.ptn,
                    'Série': produto.serie,
                    'Data de Entrada': produto.data_entrada.strftime('%d/%m/%Y'),
                    'Defeito Específico': produto.defeito_especifico,
                    'SKU': sku,
                    'Modelo': modelo,
                    'Sufixo': sufixo,

                    # Dados dos responsáveis
                    'Responsável Entrada': responsavel_entrada,
                    'Responsável Triagem': responsavel_triagem,
                    'Responsável Peças': responsavel_pecas,

                    # Dados das peças vazios
                    'Número do Pedido': '',
                    'Nome da Peça': '',
                    'Defeito da Peça': '',
                    'Tipo da Peça': '',
                    'Status da Peça': '',
                })

        # Criando DataFrame com os dados coletados
        df = pd.DataFrame(dados_os)

        # Gerando o arquivo Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="ordem_de_servico.xlsx"'

        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Ordem de Serviço', index=False)

            workbook = writer.book
            worksheet = writer.sheets['Ordem de Serviço']

            # Ajustando a largura das colunas
            for col_num, value in enumerate(df.columns):
                worksheet.set_column(col_num, col_num, 20)

            # Adicionando formato ao cabeçalho
            header_format = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': 'blue'})
            for col_num, value in enumerate(df.columns):
                worksheet.write(0, col_num, value, header_format)

            # Adicionando bordas aos dados
            border_format = workbook.add_format({'border': 1})
            for row in range(1, len(df) + 1):
                for col in range(len(df.columns)):
                    worksheet.write(row, col, df.iloc[row - 1, col], border_format)

        # Marcar os produtos como impressos
        Produto.objects.filter(impresso=False).update(impresso=True)

        return response

    except Exception as e:
        messages.error(request, f'Erro ao gerar OS: {str(e)}')
        return redirect('home')  # Redireciona para a página inicial
