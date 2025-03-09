from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password

# Create your views here.
def logar(request):
    if request.method == "GET":
        return render(request, 'login_cadastro.html')
    
    elif request.method == "POST":
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')

        try:
            usuario = Usuario.objects.get(nome=nome)

            # Verifica se a senha digitada bate com a senha armazenada
            if check_password(senha, usuario.senha):
                # Aqui você pode adicionar a lógica para autenticar o usuário (exemplo: criar uma sessão)
                request.session['usuario_id'] = usuario.id
                return redirect('home')  # Redireciona para a home após login bem-sucedido
            else:
                messages.error(request, 'Usuário ou senha incorretos')
                return render(request, 'login_cadastro.html')

        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário ou senha incorretos')
            return render(request, 'login_cadastro.html')

def cadastro(request):
    if request.method =="GET":
        return render(request, 'login_cadastro.html')
    elif request.method =="POST":
        
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if Usuario.objects.filter(nome=nome).exists():
            messages.add_message(request, constants.ERROR, 'Usuário já existe')
            return render(request, 'login_cadastro.html')
        elif senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não são iguais')
            return render(request, 'login_cadastro.html')
        

        usuario = Usuario(nome=nome)
        usuario.set_password(senha)
        usuario.save()
        messages.add_message(request, constants.SUCCESS, 'Usuário Cadastrado')
        return render(request, 'login_cadastro.html')
            




