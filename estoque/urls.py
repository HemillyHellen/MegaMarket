from django.urls import path
from . import views
from django.conf.urls import include 
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Login
    # path('login/', views.login_view, name='login'),

    # Logout
    # path('logout/', views.logout_view, name='logout'),

    path('', views.dashboard, name='dashboard'),

    # Funcionários
    path('funcionarios/cadastro/', views.cadastro_funcionario, name='cadastro_funcionario'),
    path('funcionarios/listagem/', views.listagem_funcionario, name='listagem_funcionario'),
    path('funcionarios/edicao/<int:id>/', views.edicao_funcionario, name='edicao_funcionario'),
    path('funcionarios/exclusao/<int:id>/', views.exclusao_funcionario, name='exclusao_funcionario'),

    # Fornecedores
    path('fornecedores/cadastro/', views.cadastro_fornecedor, name='cadastro_fornecedor'),
    path('fornecedores/listagem/', views.listagem_fornecedor, name='listagem_fornecedor'),
    path('fornecedores/edicao/<int:id>/', views.edicao_fornecedor, name='edicao_fornecedor'),
    path('fornecedores/exclusao/<int:id>/', views.exclusao_fornecedor, name='exclusao_fornecedor'),

    # Produtos
    path('produtos/cadastro/', views.cadastro_produto, name='cadastro_produto'),
    path('produtos/listagem/', views.listagem_produto, name='listagem_produto'),
    path('produtos/edicao/<int:id>/', views.edicao_produto, name='edicao_produto'),
    path('produtos/exclusao/<int:id>/', views.exclusao_produto, name='exclusao_produto'),

    # Movimentações
    path('movimentacoes/cadastro/', views.cadastro_movimentacao, name='cadastro_movimentacao'),
    path('movimentacoes/listagem/', views.listagem_movimentacao, name='listagem_movimentacao'),
    path('movimentacoes/edicao/<int:id>/', views.edicao_movimentacao, name='edicao_movimentacao'),
    path('movimentacoes/exclusao/<int:id>/', views.exclusao_movimentacao, name='exclusao_movimentacao'),

    # Envio de email
    path('envio-email/', views.envio_email, name='envio_email'),

    # Login e Logout bugado
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/login/', views.login_view, name='login'),
]
