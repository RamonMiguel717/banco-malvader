# WARNING: Este código depende do MySQL estar rodando e do arquivo .env estar corretamente configurado.

import unittest
from unittest.mock import patch, MagicMock
from repository.contasDAO import (
    ContaRepository,
    ContaPoupancaRepository,
    ContaCorrenteRepository,
    ContaInvestimentoRepository,
    TransacaoRepository
)


class TestContaRepository(unittest.TestCase):
    @patch('repository.contasDAO.DBContext')
    def test_insert_conta(self, mock_db):
        mock_cursor = MagicMock()
        mock_db.return_value.__enter__.return_value = (None, mock_cursor)

        ContaRepository.insert_conta('12345', 1, 1000.0, 'corrente', 1, '2024-01-01', 'ativa')
        mock_cursor.execute.assert_called_once()

    @patch('repository.contasDAO.DBContext')
    def test_get_contas_by_cliente(self, mock_db):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{'id_conta': 1}]
        mock_db.return_value.__enter__.return_value = (None, mock_cursor)

        result = ContaRepository.get_contas_by_cliente(1)
        self.assertEqual(result, [{'id_conta': 1}])
        mock_cursor.execute.assert_called_once()

    @patch('repository.contasDAO.DBContext')
    def test_list_contas(self, mock_db):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{'id_conta': 1}]
        mock_db.return_value.__enter__.return_value = (None, mock_cursor)

        result = ContaRepository.list_contas()
        self.assertEqual(result, [{'id_conta': 1}])
        mock_cursor.execute.assert_called_once()

    @patch('repository.contasDAO.DBContext')
    def test_update_conta(self, mock_db):
        mock_cursor = MagicMock()
        mock_db.return_value.__enter__.return_value = (None, mock_cursor)

        ContaRepository.update_conta(1, 2000.0, 'ativa')
        mock_cursor.execute.assert_called_once()

    @patch('repository.contasDAO.DBContext')
    def test_delete_conta(self, mock_db):
        mock_cursor = MagicMock()
        mock_db.return_value.__enter__.return_value = (None, mock_cursor)

        ContaRepository.delete_conta(1)
        mock_cursor.execute.assert_called_once()


class TestContaPoupancaRepository(unittest.TestCase):
    @patch('repository.contasDAO.DBContext')
    def test_insert_conta_poupanca(self, mock_db):
        mock_cursor = MagicMock()
        mock_db.return_value.__enter__.return_value = (None, mock_cursor)

        ContaPoupancaRepository.insert_conta_poupanca(1, 0.05, '2024-01-01')
        mock_cursor.execute.assert_called_once()

    @patch('repository.contasDAO.DBContext')
    def test_update_conta_poupanca(self, mock_db):
        mock_cursor = MagicMock()
        mock_db.return_value.__enter__.return_value = (None, mock_cursor)

        ContaPoupancaRepository.update_conta_poupanca(1, 0.06, '2024-02-01')
        mock_cursor.execute.assert_called_once()


class TestContaCorrenteRepository(unittest.TestCase):
    @patch('repository.contasDAO.DBContext')
    def test_insert_conta_corrente(self, mock_db):
        mock_cursor = MagicMock()
        mock_db.return_value.__enter__.return_value = (None, mock_cursor)

        ContaCorrenteRepository.insert_conta_corrente(1, 500.0, '2025-12-31', 20.0)
        mock_cursor.execute.assert_called_once()

    @patch('repository.contasDAO.DBContext')
    def test_update_conta_corrente(self, mock_db):
        mock_cursor = MagicMock()
        mock_db.return_value.__enter__.return_value = (None, mock_cursor)

        ContaCorrenteRepository.update_conta_corrente(1, 600.0, '2025-12-31', 25.0)
        mock_cursor.execute.assert_called_once()


class TestContaInvestimentoRepository(unittest.TestCase):
    @patch('repository.contasDAO.DBContext')
    def test_insert_conta_investimento(self, mock_db):
        mock_cursor = MagicMock()
        mock_db.return_value.__enter__.return_value = (None, mock_cursor)

        ContaInvestimentoRepository.insert_conta_investimento(1, 'moderado', 1000.0, 0.08)
        mock_cursor.execute.assert_called_once()

    @patch('repository.contasDAO.DBContext')
    def test_update_conta_investimento(self, mock_db):
        mock_cursor = MagicMock()
        mock_db.return_value.__enter__.return_value = (None, mock_cursor)

        ContaInvestimentoRepository.update_conta_investimento(1, 'agressivo', 2000.0, 0.1)
        mock_cursor.execute.assert_called_once()


class TestTransacaoRepository(unittest.TestCase):
    @patch('repository.contasDAO.DBContext')
    def test_insert_transacao(self, mock_db):
        mock_cursor = MagicMock()
        mock_db.return_value.__enter__.return_value = (None, mock_cursor)

        TransacaoRepository.insert_transacao(
            1, 2, 'transferencia', 500.0, '2024-05-01 10:00:00', 'Teste de transação'
        )
        mock_cursor.execute.assert_called_once()


if __name__ == '__main__':
    unittest.main()
