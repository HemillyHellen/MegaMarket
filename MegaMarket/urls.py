"""
URL configuration for MegaMarket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from estoque import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  # Defina a URL raiz para a página de login
    path('accounts/', include('django.contrib.auth.urls')),  # URL padrão para autenticação
    path('dashboard/gerente/', views.dashboard_gerente, name='dashboard_gerente'),
    path('dashboard/funcionario/', views.dashboard_funcionario, name='dashboard_funcionario'),
    path('funcionarios/cadastro/', views.cadastro_funcionario, name='cadastro_funcionario'),
    path('funcionarios/listagem/', views.listagem_funcionario, name='listagem_funcionario'),
    path('funcionarios/edicao/<int:id>/', views.edicao_funcionario, name='edicao_funcionario'),
    path('funcionarios/exclusao/<int:id>/', views.exclusao_funcionario, name='exclusao_funcionario'),
    path('envio-email/', views.envio_email, name='envio_email'),
]