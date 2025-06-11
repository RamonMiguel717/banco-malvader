# TODO: definir uma classe para agrupar os métodos
# FIXME: Decoradores @staticmethod não podem ser usados fora de uma classe.

from .conexao import DBContext
from utils import auxiliares

class ClienteRepository:
    @staticmethod
    def insert_cliente(id_usuario,score_credito):
        with DBContext() as (_, cursor):
            cursor.execute("""
            INSERT INTO cliente (id_usuario,score_credito) VALUES (%s,%s)
        """,(id_usuario,score_credito))
            
    @staticmethod
    def recalc_score_credito(id_cliente):
        with DBContext() as (_, cursor):
            cursor.callproc("calcular_score_credito",[id_cliente])

    @staticmethod
    def get_cliente_by_cpf(cpf):
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT c.*
                FROM cliente c
                JOIN usuario u ON c.id_usuario = u.id_usuario
                WHERE u.cpf = %s
            """, (cpf,))
            return cursor.fetchone()


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
    def get_dados_completos_cliente(id_cliente):
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT u.nome, u.cpf, u.data_nascimento, u.telefone, u.tipo_usuario,
                        e.cep, e.local, e.numero_casa, e.bairro, e.cidade, e.estado,
                        c.score_credito
                FROM cliente c
                JOIN usuario u ON c.id_usuario = u.id_usuario
                JOIN endereco e ON u.id_usuario = e.id_usuario
                WHERE c.id_cliente = %s
            """, (id_cliente,))
            return cursor.fetchone()


    @staticmethod
    def list_clientes():
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT c.id_cliente, u.nome, u.cpf, u.data_nascimento, u.telefone, c.score_credito
                FROM cliente c
                JOIN usuario u ON c.id_usuario = u.id_usuario
            """)
            return cursor.fetchall()


    @staticmethod
    def update_cliente(id_cliente,novo_score):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE cliente SET score_credito = %s WHERE id_cliente = %s
        """,(novo_score,id_cliente))

    @staticmethod
    def list_contas_do_cliente(id_cliente):
        with DBContext() as (_, cursor):    
            cursor.execute("""
                SELECT numero_conta, tipo_conta, saldo, status
                FROM conta
                WHERE id_cliente = %s
            """, (id_cliente,))
            return cursor.fetchall()


    @staticmethod    
    def delete_cliente(id_cliente):
        with DBContext() as (_, cursor):
            cursor.execute("""

                SELECT COUNT(*) AS total_contas
                FROM conta
                WHERE id_cliente = %s
            """, (id_cliente))
            
            resultado = cursor.fetchone()

            if resultado['total_contas'] > 0:
                raise Exception("Não é possível apagar o cliente, ainda existem contas ativas.")
            
            cursor.execute("""
            SELECT id_usuario FROM cliente
            WHERE id_cliente = %s
            """, (id_cliente,))
            usuario = cursor.fetchone
            if not usuario:
                raise Exception("Cliente não encontrado.")
            id_usuario = usuario['id_usuario']

            cursor.execute("DELETE FROM cliente WHERE id_cliente = %s",(id_cliente,))
            cursor.execute("DELETE FROM usuario WHERE id_usuario = %s",(id_usuario,))