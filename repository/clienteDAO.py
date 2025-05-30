from conexao import DBContext
from utils import auxiliares

@staticmethod
def insert_cliente(id_usuario,score_credito):
    with DBContext() as (_, cursor):
        cursor.execute("""
        INSERT INTO cliente (id_usuario,score_credito) VALUES (%s,%s)
    """,(id_usuario,score_credito))

@staticmethod
def get_cliente_by_cpf(cpf):
    with DBContext() as (_, cursor):
        cursor.execute("""
            SELECT * FROM cliente
            WHERE id_cliente = %s
        """, (cpf,))
        resultado = cursor.fetchone()
    return resultado  

@staticmethod
def get_cliente_by_id(id_cliente):
    with DBContext() as (_, cursor):
        cursor.execute("""
            SELECT * FROM cliente
            WHERE id_cliente = %s
        """, (id_cliente,))
        resultado = cursor.fetchone()
    return resultado  


@staticmethod
def list_clientes():
    with DBContext() as (_, cursor):
        cursor.execute("SELECT * FROM cliente")
        return cursor.fetchall()
@staticmethod
def update_cliente(id_cliente,novo_score):
    with DBContext() as (_, cursor):
        cursor.execute("""
            UPDATE cliente SET score_credito = %s WHERE id_cliente = %s
    """,(novo_score,id_cliente))
    
@staticmethod    
def delete_cliente(id_cliente):
    with DBContext() as (_, cursor):
        cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (id_cliente,))