from django.shortcuts import render, get_object_or_404
from funcionario.models import Funcionario
from produto.models import Produto
from django.utils import timezone
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.

def encerrar(request):
    funcionarios = Funcionario.objects.all()
    if request.method == "GET":
        return render(request, 'saida.html', {'funcionarios': funcionarios})
    
    elif request.method == "POST":
        ptns = request.POST.getlist('ptn')
        registro = request.POST.get('registro')
        funcionario_id = request.POST.get('funcionario_id')
        funcionario = get_object_or_404(Funcionario, id=funcionario_id)

        # Lista para armazenar as mensagens de status
        status_mensagens = []

        for ptn in ptns:
            # Buscando o produto pelo PTN
            produto = Produto.objects.filter(ptn=ptn).first()  # Pega o primeiro ou None

            if produto:
                produto.responsavel_saida = funcionario
                produto.data_saida = timezone.now()
                produto.registro_saida = registro
                produto.status = "ENCERRADO"
                produto.save()
                status_mensagens.append(f"Produto com PTN {ptn} atualizado.")
            else:
                status_mensagens.append(f"⚠ Produto com PTN {ptn} não encontrado.")
        
        # Passando os funcionários e as mensagens de status para o template
        messages.add_message(request, constants.SUCCESS, 'Produto Encerrado')
        return render(request, 'saida.html', {'funcionarios': funcionarios, 'status_mensagens': status_mensagens})

    # Caso o método não seja GET ou POST, apenas retorna o template.
    return render(request, 'saida.html', {'funcionarios': funcionarios})
        


