from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario, Fornecedor, Produto, Movimentacao
from django.core.mail import send_mail
from django.http import HttpResponse
from .decorators import gerente_required
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts/login')
    
#Tentando fazer a manivela mas nn tá dando certo
def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = Usuario.objects.filter(username=username).first()
        print(usuario)
        print(usuario.is_anonymous)
        print(usuario.is_authenticated)
        print(usuario.is_active)
        print(usuario._meta)
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'registration/login.html')
    return redirect('/')

# Dashboard
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# Cadastro de funcionário
#@login_required
@gerente_required
@login_required
def cadastro_funcionario(request):
    
    if request.method == "POST":
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        
        novo_funcionario = Usuario.objects.create_user(
            username=nome,
            email=email,
            password=senha,
            usu_tipo=Usuario.FUNCIONARIO,
            usu_ger_id=Usuario.objects.filter(id=request.user.id).first()

        )
        novo_funcionario.save()
        return redirect('listagem_funcionario')
    
    return render(request, 'gerente/funcionario/cadastro.html')

# Listagem de funcionários
@gerente_required
@login_required
def listagem_funcionario(request):
    funcionarios = Usuario.objects.filter(usu_tipo=Usuario.FUNCIONARIO)
    return render(request, 'gerente/funcionario/listagem.html', {'funcionarios': funcionarios})

# Edição de funcionário
@gerente_required
@login_required
def edicao_funcionario(request, id):
    
    funcionario = get_object_or_404(Usuario, id=id)
    if request.method == "POST":
        column = request.POST.get('column')
        value = request.POST.get('value')

        # verifica se column está entre as colunas de movimentações
        if column in [field.name for field in Usuario._meta.get_fields()]:
            setattr(funcionario,column,value)
        funcionario.save()
        return redirect('listagem_funcionario')

    return render(request, 'gerente/funcionario/edicao.html', {'funcionario': funcionario})

# Exclusão de funcionário
@gerente_required
@login_required
def exclusao_funcionario(request, id):
    funcionario = get_object_or_404(Usuario, id=id)
    funcionario.delete()
    return redirect('listagem_funcionario')

# Cadastro de fornecedores
@gerente_required
@login_required
def cadastro_fornecedor(request):
    
    if request.method == "POST":
        nome = request.POST['nome']
        contato = request.POST['contato']
        email = request.POST['email']
        ger_id = Usuario.objects.filter(id=request.POST['ger_id']).first()
        
        
        novo_fornecedor = Fornecedor.objects.create(
            for_nome=nome,
            for_contato=contato,
            for_email=email,
            for_ger_id=ger_id
        )
        messages.success(request, "Fornecedor cadastrado com sucesso!")
        return redirect('listagem_fornecedor')
    
    return render(request, 'gerente/fornecedor/cadastro.html')

#listagem de fornecedores
@gerente_required
@login_required
def listagem_fornecedor(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'gerente/fornecedor/listagem.html', {'fornecedores': fornecedores})

# Edição de fornecedores
@gerente_required
@login_required
def edicao_fornecedor(request, id):
    
    fornecedor = get_object_or_404(Fornecedor, for_id=id)
    if request.method == "POST":
        column = request.POST.get('column')
        value = request.POST.get('value')

        # verifica se column está entre as colunas de produto
        if column in [field.name for field in Fornecedor._meta.get_fields()]:
            setattr(fornecedor,column,value)

        fornecedor.save()
        return redirect('listagem_fornecedor')

    return render(request, 'gerente/fornecedor/edicao.html', {'fornecedor': fornecedor})

# Exclusão de fornecedor
@gerente_required
@login_required
def exclusao_fornecedor(request, id):
    
    fornecedor = get_object_or_404(Fornecedor, for_id=id)
    fornecedor.delete()
    return redirect('listagem_fornecedor')

# Cadastro de produto.
@gerente_required
@login_required
def cadastro_produto(request):
    
    if request.method == "POST":
        nome = request.POST['nome']
        codigo = request.POST['codigo']
        descricao = request.POST['descricao']
        categoria = request.POST['categoria']
        precoCompra = request.POST['precoCompra']
        precoVenda = request.POST['precoVenda']
        qtdMinima = request.POST['qtdMinima']
        prazoValidade = request.POST['prazoValidade']
        local = request.POST['local']
        fornecedor = Fornecedor.objects.filter(for_id=request.POST['fornecedor']).first()
        
        novo_produto = Produto.objects.create(
            pro_nome=nome,
            pro_quantidade=1,
            pro_codigo=codigo,
            pro_descricao=descricao,
            pro_categoria=categoria,
            pro_precoCompra=precoCompra,
            pro_precoVenda=precoVenda,
            pro_qtdMinima=qtdMinima,
            pro_prazoValidade=prazoValidade,
            pro_local=local,
            pro_for_id=fornecedor,
            pro_usu_id=Usuario.objects.filter(id=request.user.id).first()
        )
        messages.success(request, "Produto cadastrado com sucesso!")
        return redirect('listagem_produto')
    
    fornecedores = Fornecedor.objects.all()
    return render(request, 'produto/cadastro.html', {'fornecedores': fornecedores})

# Listagem dos produtos
@login_required
def listagem_produto(request):
    produtos = Produto.objects.all()
    return render(request, 'produto/listagem.html', {'produtos': produtos})

# Edição de produto
@gerente_required
@login_required
def edicao_produto(request, id):
    
    produto = get_object_or_404(Produto, pro_id=id)
    if request.method == "POST":
        column = request.POST.get('column')
        value = request.POST.get('value')

        # verifica se column está entre as colunas de produto
        if column in [field.name for field in Produto._meta.get_fields()]:
            setattr(produto,column,value)

        produto.save()
        return redirect('listagem_produto')

    return render(request, 'produto/edicao.html', {'produto': produto})

# Exclusão de produto
@gerente_required
@login_required
def exclusao_produto(request, id):
    
    produto = get_object_or_404(Produto, pro_id=id)
    produto.delete()
    return redirect('listagem_produto')

# Cadastro de movimentacao
@gerente_required
@login_required
def cadastro_movimentacao(request):
    
    if request.method == "POST":
        tipo = request.POST['tipo']
        quantidade = request.POST['quantidade']
        data = request.POST['data']
        produto = Produto.objects.filter(pro_id=request.POST['pro_id']).first()
        
        novo_movimentacao = Movimentacao.objects.create(
            mov_tipo=tipo,
            mov_quantidade=quantidade,
            mov_data=data,
            mov_pro_id=produto,
            mov_usu_id=Usuario.objects.filter(id=request.user.id).first()

        )
        messages.success(request, "Movimentação cadastrada com sucesso!")
        return redirect('listagem_movimentacao')
    produtos = Produto.objects.all()
    return render(request, 'produto/movimentacao/cadastro.html', {'produtos':produtos})

# Listagem das movimentacoes
@gerente_required
@login_required
def listagem_movimentacao(request):
    movimentacoes = Movimentacao.objects.all()
    return render(request, 'produto/movimentacao/listagem.html', {'movimentacoes': movimentacoes})

# Edição de movimentacao
@gerente_required
@login_required
def edicao_movimentacao(request, id):
    
    movimentacao = get_object_or_404(Movimentacao, mov_id=id)
    if request.method == "POST":
        column = request.POST.get('column')
        value = request.POST.get('value')

        # verifica se column está entre as colunas de movimentações
        if column in [field.name for field in Movimentacao._meta.get_fields()]:
            setattr(movimentacao,column,value)
        movimentacao.save()
        return redirect('listagem_movimentacao')

    return render(request, 'produto/movimentacao/edicao.html', {'movimentacao': movimentacao})

#teste
# Exclusão de movimentacao
@gerente_required
@login_required
def exclusao_movimentacao(request, id):
    
    movimentacao = get_object_or_404(Movimentacao, mov_id=id)
    movimentacao.delete()
    return redirect('listagem_movimentacao')

# Envio de email
@login_required
def envio_email(request):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_usuario = "gerenciamentoestoque63@gmail.com"
    email_senha = "gerenci@123_estoque"
    if request.method == "POST":
        destinatario = request.POST['email']
        mensagem = request.POST['descricao']

        message = MIMEMultipart()
        message['From'] = email_usuario
        message["To"] = destinatario
        message["Subject"] = 'Email da empresa'
        message.attach(MIMEText(mensagem, "plain"))
        try:
        
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls() 
            server.login(email_usuario, email_senha)
            server.sendmail(email_usuario, destinatario, message.as_string())
            print("E-mail enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
        finally:
            server.quit()
        return HttpResponse("Email enviado com sucesso!")
    users = Usuario.objects.all()
    return render(request, 'envio_email.html', {'users':users})