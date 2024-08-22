import factory
from estoque.models import Produto, Usuario, Fornecedor
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class UsuarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Usuario

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    usu_tipo = factory.Iterator([Usuario.GERENTE, Usuario.FUNCIONARIO])  # Pode alternar entre tipos
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')

    @factory.post_generation
    def setup_password(obj, create, extracted, **kwargs):
        if extracted:
            obj.set_password(extracted)
        else:
            obj.set_password('defaultpassword')

class FornecedorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'estoque.Fornecedor'

    for_nome = factory.Faker('company')
    for_email = factory.Faker('company_email')
    for_contato = factory.Faker('phone_number')
    for_ger_id = factory.SubFactory(UsuarioFactory, usu_tipo=Usuario.GERENTE)
    
class ProdutoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'estoque.Produto'

    pro_nome = factory.Faker('word')
    pro_quantidade = factory.Faker('random_int', min=0, max=100)
    pro_codigo = factory.Faker('ean13')
    pro_descricao = factory.Faker('text', max_nb_chars=200)
    pro_categoria = factory.Faker('word')
    pro_precoCompra = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    pro_precoVenda = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    pro_qtdMinima = factory.Faker('random_int', min=1, max=10)
    pro_prazoValidade = factory.Faker('date')
    pro_local = factory.Faker('word')
    pro_for_id = factory.SubFactory(FornecedorFactory)
    pro_usu_id = factory.SubFactory(UsuarioFactory, usu_tipo=Usuario.FUNCIONARIO)

class MovimentacaoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'estoque.Movimentacao'

    mov_tipo = factory.Iterator(['entrada', 'saida'])
    mov_quantidade = factory.Faker('random_int', min=1, max=100)
    mov_data = factory.Faker('date_time_this_year')
    mov_pro_id = factory.SubFactory(ProdutoFactory)
    mov_usu_id = factory.SubFactory(UsuarioFactory)

    