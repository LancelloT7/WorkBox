from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from produto.models import Produto
from pecas.models import ProdutoPeca  # Certifique-se de importar o modelo correto
import pandas as pd

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
