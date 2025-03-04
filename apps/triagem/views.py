from django.shortcuts import render, get_object_or_404
from produto.models import Produto
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.messages import constants


def cad_triagem(request):
    if request.method == "GET":
        return render(request, 'triagem.html')
    
    if request.method == "POST":
        try:
            ptn = request.POST.get('ptn').upper()
            produto = Produto.objects.get(ptn=ptn)  
            return render(request, 'form_triagem.html', {'produto': produto, 'defeito_especifico_choices': Produto.DEFEITO_ESPECIFICO})
        except Produto.DoesNotExist:
            messages.add_message(request, constants.ERROR, 'Produto não encontrado')
            return render(request, 'triagem.html')



    
    

def buscar(request):
    ptn = request.GET.get('ptn', None).upper()
    if ptn:
        produto = get_object_or_404(Produto, ptn=ptn)
        data = {
            'status': produto.status,
            'data_entrada': produto.data_entrada.strftime('%d/%m/%Y %H:%M'),
            'responsavel_entrada': produto.responsavel_entrada.nome if produto.responsavel_entrada else 'Não atribuído',
            'ptn': produto.ptn,
            'serie': produto.serie,
            'sku': produto.sku.id if produto.sku else 'N/A',
            'sufixo': produto.sufixo.id if produto.sufixo else 'N/A',
            'modelo': produto.modelo.id if produto.modelo else 'N/A',
            'defeito': produto.tipo_defeito,
            'responsavel_conserto': produto.responsavel_conserto.nome if produto.responsavel_conserto else 'Não atribuído',
            'responsavel_embalagem': produto.responsavel_embalagem.nome if produto.responsavel_embalagem else 'Não atribuído',
            'responsavel_entrada': produto.responsavel_entrada.nome if produto.responsavel_entrada else 'Não atribuído',
            'responsavel_saida': produto.responsavel_saida.nome if produto.responsavel_saida else 'Não atribuído',
            'responsavel_triagem': produto.responsavel_triagem.nome if produto.responsavel_triagem else 'Não atribuído',
        }
        return JsonResponse(data)

    return JsonResponse({'erro': 'Código não informado'}, status=400)


def form_triagem(request):
    if request.method == "POST":
        ptn = request.POST.get('ptn').upper()
        produto = get_object_or_404(Produto, ptn=ptn)
        produto.defeito_especifico = request.POST.get('defeito_especifico')
        produto.status = 'TRIAGEM'  # Corrigido
        produto.save()
        messages.add_message(request, constants.SUCCESS, 'Triagem Cadastrada')
        return render(request, 'triagem.html')




        
        
