from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    GERENTE = 'gerente'
    FUNCIONARIO = 'funcionario'
    TIPOS_USUARIO = [
        (GERENTE, 'Gerente'),
        (FUNCIONARIO, 'Funcionário'),
    ]
    
    usu_tipo = models.CharField(max_length=20, choices=TIPOS_USUARIO)
    usu_ger_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='funcionarios')

    def save(self, *args, **kwargs):
        if self.pk is None and not self.is_superuser:
            self.set_password(self.password)  
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.username} ({self.get_usu_tipo_display()})'

class Fornecedor(models.Model):
    for_id = models.AutoField(primary_key=True)
    for_nome = models.CharField(max_length=255)
    for_contato = models.CharField(max_length=255)
    for_email = models.EmailField()
    for_ger_id = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'usu_tipo': Usuario.GERENTE})

class Produto(models.Model):
    pro_id = models.AutoField(primary_key=True)
    pro_nome = models.CharField(max_length=255)
    pro_quantidade = models.IntegerField()
    pro_codigo = models.CharField(max_length=255, unique=True)
    pro_descricao = models.TextField()
    pro_categoria = models.CharField(max_length=255)
    pro_precoCompra = models.DecimalField(max_digits=10, decimal_places=2)
    pro_precoVenda = models.DecimalField(max_digits=10, decimal_places=2)
    pro_qtdMinima = models.IntegerField()
    pro_prazoValidade = models.DateField()
    pro_local = models.CharField(max_length=255)
    pro_for_id = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    pro_usu_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Movimentacao(models.Model):
    ENTRADA = 'entrada'
    SAIDA = 'saida'
    TIPOS_MOVIMENTACAO = [
        (ENTRADA, 'Entrada'),
        (SAIDA, 'Saída'),
    ]

    mov_id = models.AutoField(primary_key=True)
    mov_tipo = models.CharField(max_length=10, choices=TIPOS_MOVIMENTACAO)
    mov_quantidade = models.IntegerField()
    mov_data = models.DateTimeField(auto_now_add=True)
    mov_pro_id = models.ForeignKey(Produto, on_delete=models.CASCADE)
    mov_usu_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)