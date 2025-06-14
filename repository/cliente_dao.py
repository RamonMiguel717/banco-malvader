from .conexao import DBContext
from datetime import datetime
from ..model.cliente_model import Cliente

class ClienteRepository:

    @staticmethod
    #INSERE as informações básicas do CLIENTE dentro da tabela de CLIENTES
    def insert_cliente(id_usuario, score_credito):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO cliente (id_usuario, score_credito)
                VALUES (%s, %s)
            """, (id_usuario, score_credito))

    @staticmethod

    def recalc_score_credito(id_cliente):
        with DBContext() as (_, cursor):
            cursor.callproc("calcular_score_credito", [id_cliente])

    @staticmethod
    #ENCONTRA as informações do cliente a partir do CPF
    def get_cliente_by_cpf(cpf):
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT c.*
                FROM cliente c
                JOIN usuario u ON c.id_usuario = u.id_usuario
                WHERE u.cpf = %s
            """, (cpf,))
            row = cursor.fetchone()
            return Cliente(**row) if row else None
        # Retorna o objeto CLIENTE como definido na camada MODEL, caso não encontre nada = NONE


    @staticmethod
    # ENCONTRA as informações da TABELA CLIENTE a partir do ID
    def get_cliente_by_id(id_cliente):
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT * FROM cliente
                WHERE id_cliente = %s
            """, (id_cliente,))
            row = cursor.fetchone()
            return Cliente(**row) if row else None
    # Retorna o objeto CLIENTE como definido na camada MODEL, caso não encontre nada = NONE

    @staticmethod
    # Encontra o score do cliente a partir do ID
    def get_score_credito(id_cliente):
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT score_credito
                FROM cliente
                WHERE id_cliente = %s
            """, (id_cliente,))
            row = cursor.fetchone()
            return row['score_credito'] if row else None
    # Retorna a informação Score do objeto CLIENTE

    #TODO atualmente ainda não há um procedure que faça um calculo de SCORE armazenado no banco de dados
    #A CLASSE AINDA NÃO FUNCIONA
    @staticmethod
    def calc_score_credito(id_cliente):
        with DBContext() as (_, cursor):
            cursor.callproc("calc_score_credito",[id_cliente]) 

    @staticmethod
    # Retorna TODOS os dados relacionados ao ID inserido
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
    # Retorna os dados do cleinte como um DICIONÁRIO (precisa desempacotar para exibir)

    @staticmethod
    # Lista as informações da tabela CLIENTE+USUARIO
    def list_clientes():
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT c.id_cliente, u.nome, u.cpf, u.data_nascimento, u.telefone, c.score_credito
                FROM cliente c
                JOIN usuario u ON c.id_usuario = u.id_usuario
            """)
            return cursor.fetchall()

    @staticmethod
    # Atualiza o score do cliente a partir do seu ID
    def update_cliente_score(id_cliente, novo_score):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE cliente
                SET score_credito = %s
                WHERE id_cliente = %s
            """, (novo_score, id_cliente))

    @staticmethod
    # Lista todas as contas relacionadas ao ID inserido
    def list_contas_do_cliente(id_cliente):
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT numero_conta, tipo_conta, saldo, status
                FROM conta
                WHERE id_cliente = %s
            """, (id_cliente,))
            return cursor.fetchall()
    # Retorna um DICIONÁRIO (desempacotar para exibir a informação)
    
    @staticmethod
    def delete_cliente(id_cliente):
        with DBContext() as (_, cursor):
            # Verifica se há contas associadas
            cursor.execute("""
                SELECT COUNT(*) AS total_contas
                FROM conta
                WHERE id_cliente = %s
            """, (id_cliente,))
            resultado = cursor.fetchone()

            if resultado and resultado['total_contas'] > 0:
                raise Exception("Não é possível apagar o cliente: ainda existem contas ativas.")

            # Busca o id_usuario associado
            cursor.execute("""
                SELECT id_usuario
                FROM cliente
                WHERE id_cliente = %s
            """, (id_cliente,))
            usuario = cursor.fetchone()

            if not usuario:
                raise Exception("Cliente não encontrado.")

            id_usuario = usuario['id_usuario']

            # Deleta cliente e usuário
            cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (id_cliente,))
            cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))

    @staticmethod
    def registrar_login(id_cliente):
        data = datetime.now()
    # TODO fazer a chamada em Auditoria inserindo o login.