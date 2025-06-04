# WARNING: Este código depende do MySQL estar rodando e do arquivo .env estar corretamente configurado.

import unittest
from repository.conexao import obter_conexao, DBContext

class TestConexao(unittest.TestCase):

    def test_obter_conexao(self):
        conn = obter_conexao()
        self.assertIsNotNone(conn)
        self.assertTrue(conn.is_connected())
        conn.close()

    def test_db_context(self):
        with DBContext() as (conn, cursor):
            self.assertIsNotNone(conn)
            self.assertIsNotNone(cursor)
            self.assertTrue(conn.is_connected())

            # Executa uma query simples
            cursor.execute("SELECT 1 AS resultado")
            resultado = cursor.fetchone()
            self.assertEqual(resultado['resultado'], 1)

        # Após sair do contexto, conexão deve estar fechada
        self.assertFalse(conn.is_connected())


if __name__ == '__main__':
    unittest.main()
