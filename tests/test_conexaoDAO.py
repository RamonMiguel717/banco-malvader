# tests/test_conexao.py
import unittest
from unittest.mock import patch, MagicMock
from repository.conexao import obter_conexao

class TestConexao(unittest.TestCase):

    @patch('repository.conexao.mysql.connector.connect')
    def test_obter_conexao(self, mock_connect):
        # Arrange
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # Act
        conn = obter_conexao()

        # Assert
        mock_connect.assert_called_once()
        self.assertEqual(conn, mock_conn)


if __name__ == '__main__':
    unittest.main()
