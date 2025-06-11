import unittest
from unittest.mock import patch, MagicMock
from repository.auditoriaDAO import AuditoriaRepository


class TestAuditoriaRepository(unittest.TestCase):

    @patch('repository.auditoriaDAO.DBContext')
    def test_insert_auditoria(self, mock_db_context):
        # Mock do cursor e do contexto
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_db_context.return_value.__enter__.return_value = (mock_conn, mock_cursor)

        # Dados fictícios
        id_usuario = 1
        acao = 'INSERT'
        data_hora = '2024-05-31 12:00:00'
        detalhes = 'Inserção de dados de teste'

        # Chamada do método que será testado
        AuditoriaRepository.insert_auditoria(id_usuario, acao, data_hora, detalhes)

        # Validação se o execute foi chamado corretamente
        mock_cursor.execute.assert_called_once_with(
            """
                INSERT INTO auditoria (id_usuario, acao, data_hora, detalhes)
                VALUES (%s, %s, %s, %s)
            """,
            (id_usuario, acao, data_hora, detalhes)
        )

if __name__ == '__main__':
    unittest.main()
