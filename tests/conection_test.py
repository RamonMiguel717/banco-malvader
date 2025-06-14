import pytest
from ..repository.conexao import DBContext

class TestConexaoBancoDados:
    def test_conexao_estabelecida(self):
        """Testa se a conexão com o banco é estabelecida com sucesso"""
        try:
            with DBContext() as (conn, _):
                assert conn.is_connected()
        except Exception as e:
            pytest.fail(f"Falha ao conectar ao banco de dados: {str(e)}")

    def test_consulta_simples(self, db_cursor):
        """Testa se consultas básicas funcionam"""
        db_cursor.execute("SELECT 1 AS resultado")
        result = db_cursor.fetchone()
        assert result['resultado'] == 1

    def test_transacao_commit(self, db_connection):
        """Testa se transações são commitadas corretamente"""
        try:
            with DBContext() as (conn, cursor):
                cursor.execute("CREATE TABLE IF NOT EXISTS teste_pytest (id INT)")
                cursor.execute("INSERT INTO teste_pytest VALUES (1)")
            
            # Verifica se o commit foi feito
            with DBContext() as (conn, cursor):
                cursor.execute("SELECT COUNT(*) AS total FROM teste_pytest")
                assert cursor.fetchone()['total'] == 1
                
        finally:
            # Limpeza
            with DBContext() as (conn, cursor):
                cursor.execute("DROP TABLE IF EXISTS teste_pytest")

    def test_rollback_em_erro(self, db_connection):
        """Testa se o rollback funciona corretamente"""
        try:
            # Cria tabela temporária
            with DBContext() as (_, cursor):
                cursor.execute("CREATE TABLE IF NOT EXISTS teste_rollback (id INT PRIMARY KEY)")
                cursor.execute("INSERT INTO teste_rollback VALUES (1)")
            
            # Força um erro
            try:
                with DBContext() as (_, cursor):
                    cursor.execute("INSERT INTO teste_rollback VALUES (1)")  # Duplicado, causa erro
                    pytest.fail("Deveria ter lançado uma exceção")
            except Exception:
                pass  # Esperado
            
            # Verifica se o rollback foi feito
            with DBContext() as (_, cursor):
                cursor.execute("SELECT COUNT(*) AS total FROM teste_rollback")
                assert cursor.fetchone()['total'] == 1  # Ainda só tem o primeiro registro
                
        finally:
            # Limpeza
            with DBContext() as (_, cursor):
                cursor.execute("DROP TABLE IF EXISTS teste_rollback")