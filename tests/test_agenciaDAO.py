import unittest # Importa o módulo de testes unitários do Python
from unittest.mock import patch, MagicMock # Importa ferramentas para criar mocks e patches (substituições temporárias) durante os testes
from repository.agenciaDAO import AgenciaRepository # Importa a classe AgenciaRepository do módulo agenciaDAO dentro do pacote repository

# Cria uma classe de teste que herda de unittest.TestCase
class TestAgenciaRepository(unittest.TestCase):

    # Testa o método de inserção de agência
    @patch('repository.agenciaDAO.DBContext')  # Substitui temporariamente DBContext por um mock
    def test_insert_agencia(self, mock_db_context):
        # Cria um mock para o cursor do banco
        mock_cursor = MagicMock()
        # Configura o mock do DBContext para retornar None e o mock_cursor ao entrar no contexto (with)
        mock_db_context.return_value.__enter__.return_value = (None, mock_cursor)

        # Executa o método que insere uma agência
        AgenciaRepository.insert_agencia('Agencia Teste', '123', 1)

        # Verifica se o método execute do cursor foi chamado com o comando SQL correto e os parâmetros certos
        mock_cursor.execute.assert_called_with("""
                INSERT INTO agencia (nome, codigo_agencia, endereco_id)
                VALUES (%s, %s, %s)
            """, ('Agencia Teste', '123', 1))

    # Testa o método de listagem de agências
    @patch('repository.agenciaDAO.DBContext')  # Substitui temporariamente DBContext por um mock
    def test_list_agencias(self, mock_db_context):
        # Cria um mock para o cursor do banco
        mock_cursor = MagicMock()
        # Define que quando fetchall() for chamado, ele vai retornar uma lista com uma tupla ('Agencia Teste',)
        mock_cursor.fetchall.return_value = [('Agencia Teste',)]
        # Configura o mock do DBContext para retornar None e o mock_cursor ao entrar no contexto (with)
        mock_db_context.return_value.__enter__.return_value = (None, mock_cursor)

        # Executa o método que lista agências
        result = AgenciaRepository.list_agencias()

        # Verifica se o método execute foi chamado com o comando SQL correto
        mock_cursor.execute.assert_called_with("SELECT * FROM agencia")
        # Verifica se o resultado retornado é igual ao esperado
        self.assertEqual(result, [('Agencia Teste',)])

    # Testa o método de atualização de uma agência
    @patch('repository.agenciaDAO.DBContext')  # Substitui temporariamente DBContext por um mock
    def test_update_agencia(self, mock_db_context):
        # Cria um mock para o cursor do banco
        mock_cursor = MagicMock()
        # Configura o mock do DBContext para retornar None e o mock_cursor ao entrar no contexto (with)
        mock_db_context.return_value.__enter__.return_value = (None, mock_cursor)

        # Executa o método que atualiza uma agência
        AgenciaRepository.update_agencia(1, 'Nova Agencia', '456')

        # Verifica se o método execute foi chamado com o comando SQL correto e os parâmetros certos
        mock_cursor.execute.assert_called_with("""
                UPDATE agencia 
                SET nome = %s, codigo_agencia = %s
                WHERE id_agencia = %s
            """, ('Nova Agencia', '456', 1))

    # Testa o método de exclusão de uma agência
    @patch('repository.agenciaDAO.DBContext')  # Substitui temporariamente DBContext por um mock
    def test_delete_agencia(self, mock_db_context):
        # Cria um mock para o cursor do banco
        mock_cursor = MagicMock()
        # Configura o mock do DBContext para retornar None e o mock_cursor ao entrar no contexto (with)
        mock_db_context.return_value.__enter__.return_value = (None, mock_cursor)

        # Executa o método que deleta uma agência
        AgenciaRepository.delete_agencia(1)

        # Verifica se o método execute foi chamado com o comando SQL correto e o parâmetro certo
        mock_cursor.execute.assert_called_with(
            "DELETE FROM agencia WHERE id_agencia = %s", (1,)
        )


# Executa os testes quando o arquivo é rodado diretamente
if __name__ == '__main__':
    unittest.main()
