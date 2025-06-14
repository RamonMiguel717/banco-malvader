import pytest
from ..repository.conexao import obter_conexao
from mysql.connector import Error

@pytest.fixture(scope="module")
def db_connection():
    """Fixture que fornece uma conexão com o banco de dados"""
    try:
        conn = obter_conexao()
        yield conn
        conn.close()
    except Error as e:
        pytest.skip(f"Não foi possível conectar ao banco de dados: {str(e)}")

@pytest.fixture
def db_cursor(db_connection):
    """Fixture que fornece um cursor para testes"""
    cursor = db_connection.cursor(dictionary=True)
    yield cursor
    cursor.close()