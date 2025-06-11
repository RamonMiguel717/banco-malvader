import unittest
from unittest.mock import patch
from repository import bancoDAO

class TestBancoDAO(unittest.TestCase):

    @patch('repository.bancoDAO.T.create_table_relatorio')
    @patch('repository.bancoDAO.T.create_table_auditoria')
    @patch('repository.bancoDAO.T.create_table_transacao')
    @patch('repository.bancoDAO.T.create_table_conta_investimentos')
    @patch('repository.bancoDAO.T.create_table_conta_corrente')
    @patch('repository.bancoDAO.T.create_table_conta_poupanca')  # ✔️ Corrigido
    @patch('repository.bancoDAO.T.create_table_conta')
    @patch('repository.bancoDAO.T.create_table_agencia')
    @patch('repository.bancoDAO.T.create_table_endereco')
    @patch('repository.bancoDAO.T.create_table_cliente')
    @patch('repository.bancoDAO.T.create_table_funcionarios')
    @patch('repository.bancoDAO.T.create_table_usuario')
    @patch('repository.bancoDAO.criar_banco')
    def test_criar_banco_e_tabelas(
        self,
        mock_criar_banco,
        mock_create_usuario,
        mock_create_funcionarios,
        mock_create_cliente,
        mock_create_endereco,
        mock_create_agencia,
        mock_create_conta,
        mock_create_conta_poupanca,  # ✔️ Corrigido nome
        mock_create_conta_corrente,
        mock_create_conta_investimentos,
        mock_create_transacao,
        mock_create_auditoria,
        mock_create_relatorio,
    ):
        # Lista de mocks para facilitar as verificações
        mocks = [
            mock_create_usuario,
            mock_create_funcionarios,
            mock_create_cliente,
            mock_create_endereco,
            mock_create_agencia,
            mock_create_conta,
            mock_create_conta_poupanca,
            mock_create_conta_corrente,
            mock_create_conta_investimentos,
            mock_create_transacao,
            mock_create_auditoria,
            mock_create_relatorio,
        ]

        for m in mocks:
            m.return_value = None

        bancoDAO.criar_banco_e_tabelas()

        mock_criar_banco.assert_called_once()
        for m in mocks:
            m.assert_called_once()


if __name__ == '__main__':
    unittest.main()
