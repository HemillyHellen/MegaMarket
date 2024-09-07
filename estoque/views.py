from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Usuario, Fornecedor, Produto, Movimentacao
from django.core.mail import send_mail
from django.http import HttpResponse

# View de login
def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        senha = request.POST['senha']
        usuario = authenticate(request, username=email, password=senha)
        if usuario is not None:
            login(request, usuario)
            if usuario.usu_tipo == Usuario.GERENTE:
                return redirect('dashboard_gerente')
            else:
                return redirect('dashboard_funcionario')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard do gerente
#@login_required
def dashboard_gerente(request):
    if request.user.usu_tipo != Usuario.GERENTE:
        return HttpResponse("Acesso negado.")
    return render(request, 'gerente/dashboard.html')

# Dashboard do funcionário
#@login_required
def dashboard_funcionario(request):
    if request.user.usu_tipo != Usuario.FUNCIONARIO:
        return HttpResponse("Acesso negado.")
    return render(request, 'funcionario/dashboard.html')

# Cadastro de funcionário
#@login_required
def cadastro_funcionario(request):
    if request.user.usu_tipo != Usuario.GERENTE:
        return HttpResponse("Acesso negado.")
    
    if request.method == "POST":
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        funcao = request.POST['funcao']
        
        novo_funcionario = Usuario.objects.create_user(
            username=email, email=email, password=senha, usu_tipo=Usuario.FUNCIONARIO)
        novo_funcionario.save()
        return redirect('listagem_funcionario')
    
    return render(request, 'gerente/funcionario/cadastro.html')

# Listagem de funcionários
@login_required
def listagem_funcionario(request):
    if request.user.usu_tipo != Usuario.GERENTE:
        return HttpResponse("Acesso negado.")
    
    funcionarios = Usuario.objects.filter(usu_tipo=Usuario.FUNCIONARIO)
    return render(request, 'gerente/funcionario/listagem.html', {'funcionarios': funcionarios})

# Edição de funcionário
@login_required
def edicao_funcionario(request, id):
    if request.user.usu_tipo != Usuario.GERENTE:
        return HttpResponse("Acesso negado.")
    
    funcionario = get_object_or_404(Usuario, id=id)
    if request.method == "POST":
        funcionario.username = request.POST['email']
        funcionario.email = request.POST['email']
        funcionario.save()
        return redirect('listagem_funcionario')

    return render(request, 'gerente/funcionario/edicao.html', {'funcionario': funcionario})

# Exclusão de funcionário
@login_required
def exclusao_funcionario(request, id):
    if request.user.usu_tipo != Usuario.GERENTE:
        return HttpResponse("Acesso negado.")
    
    funcionario = get_object_or_404(Usuario, id=id)
    funcionario.delete()
    return redirect('listagem_funcionario')

# Envio de email
#@login_required
def envio_email(request):
    if request.method == "POST":
        email = request.POST['email']
        descricao = request.POST['descricao']
        send_mail(
            'Assunto do Email',
            descricao,
            'email@dominio.com',
            [email],
            fail_silently=False,
        )
        return HttpResponse("Email enviado com sucesso!")
    
    return render(request, 'envio_email.html')

