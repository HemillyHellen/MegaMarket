from django.test import TestCase
from estoque.models import Produto
from estoque.factories import UsuarioFactory, FornecedorFactory, ProdutoFactory, MovimentacaoFactory

class ProdutoTestCase(TestCase):
    def setUp(self):
        self.gerente = UsuarioFactory(usu_tipo='gerente')
        self.funcionario = UsuarioFactory(usu_tipo='funcionario')
        self.fornecedor = FornecedorFactory(for_ger_id=self.gerente)
        self.produto = ProdutoFactory(pro_for_id=self.fornecedor, pro_usu_id=self.funcionario)

    def test_criacao_produto(self):
        self.assertTrue(isinstance(self.produto, Produto))
        self.assertEqual(self.produto.pro_for_id.for_nome, self.fornecedor.for_nome)
