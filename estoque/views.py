from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario, Fornecedor, Produto, Movimentacao, Notificacao
from django.core.mail import send_mail
from django.http import HttpResponse
from .decorators import gerente_required
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts/login')
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = Usuario.objects.filter(username=username).first()
        # print(usuario)
        # print(usuario.is_anonymous)
        # print(usuario.is_authenticated)
        # print(usuario.is_active)
        # print(usuario._meta)
        # is_valid = check_password(password, usuario.password)
        # print(is_valid)
        if usuario:
            if usuario.check_password(password):
                # print('senha checada')
                login(request, usuario)
            else:
                print('erro na checagem de senha')
        else:
            print('erro ao achar usuario')
        return redirect('/')
    else:
        return render(request, 'registration/login.html')

# Dashboard
@login_required
def dashboard(request):
    notificacoes = Notificacao.objects.all()
    return render(request, 'dashboard.html', {'notificacoes': notificacoes})

# Cadastro de funcionário
@gerente_required
@login_required
def cadastro_funcionario(request):
    if request.method == "POST":
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        try:
            funcionario = Usuario.objects.create_user(
                username=nome,
                email=email,
                usu_tipo=Usuario.FUNCIONARIO,
                usu_ger_id=Usuario.objects.filter(id=request.user.id).first()

            )
            funcionario.set_password(senha)
            funcionario.save()
            user_email = Usuario.objects.filter(id=request.user.id).first().email
            send_mail(
                    'Credenciais',
                    'Seu email: '+email+' , sua senha: '+senha,
                    user_email,
                    [email]
                )
            return redirect('listagem_funcionario')
        except:
            print ('Erro ao cadastrar o funcionário')
        
    
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
        
        Fornecedor.objects.create(
            for_nome=nome,
            for_contato=contato,
            for_email=email,
            for_ger_id=Usuario.objects.filter(id=request.user.id).first()
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
@login_required
def cadastro_produto(request):
    print(f"request.user: {request.user}, type: {type(request.user)}")
    
    if request.method == "POST":
        nome = request.POST['nome']
        codigo = request.POST['codigo']
        descricao = request.POST['descricao']
        categoria = request.POST['categoria']
        precoCompra = request.POST['precoCompra']
        precoVenda = request.POST['precoVenda']
        quantidade = request.POST['quantidade']
        qtdMinima = request.POST['qtdMinima']
        prazoValidade = request.POST['prazoValidade']
        local = request.POST['local']
        fornecedor = Fornecedor.objects.filter(for_id=request.POST['fornecedor']).first()
        
        try:
            novo_produto = Produto.objects.create(
                pro_nome=nome,
                pro_quantidade=quantidade,
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
            get_status_produto()
            return redirect('listagem_produto')
        except:
            ('Error ao cadastrar o produto!')

    fornecedores = Fornecedor.objects.all()
    return render(request, 'produto/cadastro.html', {'fornecedores': fornecedores})

# Listagem dos produtos
@login_required
def listagem_produto(request):
    produtos = Produto.objects.all()
    return render(request, 'produto/listagem.html', {'produtos': produtos})

# Edição de produto
@login_required
def edicao_produto(request, id):
    
    produto = get_object_or_404(Produto, pro_id=id)
    if request.method == "POST":
        column = request.POST.get('column')
        value = request.POST.get('value')
        if column == 'pro_for_id':
            value = Fornecedor.objects.filter(for_id=value).first()
        if column in [field.name for field in Produto._meta.get_fields()]:
            setattr(produto,column,value)

        produto.save()
        get_status_produto()
        return redirect('listagem_produto')

    fornecedores = Fornecedor.objects.all()
    return render(request, 'produto/edicao.html', {'produto': produto,'fornecedores':fornecedores})

# Exclusão de produto
@login_required
def exclusao_produto(request, id):
    
    produto = get_object_or_404(Produto, pro_id=id)
    produto.delete()
    return redirect('listagem_produto')

# Cadastro de movimentacao
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
@login_required
def listagem_movimentacao(request):
    movimentacoes = Movimentacao.objects.all()
    return render(request, 'produto/movimentacao/listagem.html', {'movimentacoes': movimentacoes})
    
# Edição de movimentacao
@login_required
def edicao_movimentacao(request, id):
    
    movimentacao = get_object_or_404(Movimentacao, mov_id=id)
    if request.method == "POST":
        column = request.POST.get('column')
        value = request.POST.get('value')

        if column in [field.name for field in Movimentacao._meta.get_fields()]:
            setattr(movimentacao,column,value)
        movimentacao.save()
        return redirect('listagem_movimentacao')

    return render(request, 'produto/movimentacao/edicao.html', {'movimentacao': movimentacao})

#teste
# Exclusão de movimentacao
@login_required
def exclusao_movimentacao(request, id):
    
    movimentacao = get_object_or_404(Movimentacao, mov_id=id)
    movimentacao.delete()
    return redirect('listagem_movimentacao')

# Envio de email
# obs.: O código comentado foi por uma tentativa de envio de emails por meio do serviço smtp
@login_required
def envio_email(request):
    user = Usuario.objects.filter(id=request.user.id).first()
    email_usuario = user.email
    # email_senha = "gerenci@123_estoque"
    if request.method == "POST":
        destinatario = request.POST['email']
        mensagem = request.POST['descricao']

        # message = MIMEMultipart()
        # message['From'] = email_usuario
        # message["To"] = destinatario
        # message["Subject"] = 'Email da empresa'
        # message.attach(MIMEText(mensagem, "plain"))
        try:
            send_mail(
                'Assunto',
                mensagem,
                email_usuario,
                [destinatario]
            )
            # Conexão com o servidor
            # server = smtplib.SMTP("smtp.office365.com", 25)
            # server.starttls()  # Inicia comunicação criptografada
            # server.login(email_usuario, email_senha)
            # server.sendmail(email_usuario, destinatario, message.as_string())
            print("E-mail enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
        # finally:
        #     server.quit()
    users = Usuario.objects.all()
    return render(request, 'envio_email.html', {'users':users})


def get_status_produto():
    notificacoes = Notificacao.objects.all()
    for item in notificacoes:
        item.delete()
    else:
        produtos = Produto.objects.all()
        for item in produtos: 
            data_hora_atual = datetime.now().date()
            dias_para_vencer = item.pro_prazoValidade - data_hora_atual
            if item.pro_quantidade < item.pro_qtdMinima:
                Notificacao.objects.create(not_mensagem=f'O produto {item.pro_nome} está em falta',not_pro_id=item)
            if dias_para_vencer.days < 1:
                Notificacao.objects.create(not_mensagem=f'O produto {item.pro_nome} está vencido',not_pro_id=item)
            if item.pro_descricao == 'qualidade afetada':
                Notificacao.objects.create(not_mensagem=f'O produto {item.pro_nome} está em com a qualidade afetada',not_pro_id=item)

@login_required
def exclusao_notificacao(id):
    notificacao = get_object_or_404(Notificacao, id=id)
    notificacao.delete()
    return redirect('/')



# Relatório de produtos
@login_required
def gerar_relatorio_produtos(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_produtos.pdf"'


    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []


    title = Paragraph("Relatório de Produtos", styles['Title'])
    user_info = Paragraph(f"Gerado por: {request.user.username}", styles['Normal'])
    description = Paragraph("Lista de produtos cadastrados:", styles['Normal'])


    elements.extend([title, Spacer(1, 12), user_info, Spacer(1, 12), description, Spacer(1, 24)])


    produtos = Produto.objects.all()
    data = [["Nome", "Código", "Categoria", "Quantidade", "Qtd. Mínima", "Prazo Validade"]]


    for produto in produtos:
        data.append([
            produto.pro_nome,
            produto.pro_codigo,
            produto.pro_categoria,
            produto.pro_quantidade,
            produto.pro_qtdMinima,
            produto.pro_prazoValidade,
        ])


    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))


    elements.append(table)


    doc.build(elements)
    return response

# Relatório de alertas
@login_required
def gerar_relatorio_alertas(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_produtos.pdf"'


    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []


    title = Paragraph("Relatório de Alertas", styles['Title'])
    user_info = Paragraph(f"Gerado por: {request.user.username}", styles['Normal'])
    description = Paragraph("Lista de alertas:", styles['Normal'])


    elements.extend([title, Spacer(1, 12), user_info, Spacer(1, 12), description, Spacer(1, 24)])


    alertas = Notificacao.objects.all()
    data = [["Mensagem",'Produto']]


    for item in alertas:

        data.append([
            item.not_mensagem,
            item.not_pro_id.pro_nome
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    doc.build(elements)
    return response