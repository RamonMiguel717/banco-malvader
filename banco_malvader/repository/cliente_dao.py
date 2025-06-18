from banco_malvader.conexao import DBContext
from datetime import datetime
from banco_malvader.model.cliente_model import Cliente


class ClienteRepository:

    @staticmethod
    def insert_cliente(cliente: Cliente):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO cliente (id_usuario, score_credito)
                VALUES (%s, %s)
            """, (cliente.id_usuario, cliente.score_credito))

    @staticmethod
    def recalc_score_credito(id_cliente: int):
        with DBContext() as (_, cursor):
            cursor.callproc("calcular_score_credito", [id_cliente])

    @staticmethod
    def get_cliente_by_cpf(cpf: str) -> Cliente | None:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT c.*
                FROM cliente c
                JOIN usuario u ON c.id_usuario = u.id_usuario
                WHERE u.cpf = %s
            """, (cpf,))
            row = cursor.fetchone()
            return Cliente(**row) if row else None

    @staticmethod
    def get_cliente_by_id(id_cliente: int) -> Cliente | None:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT * FROM cliente
                WHERE id_cliente = %s
            """, (id_cliente,))
            row = cursor.fetchone()
            return Cliente(**row) if row else None

    @staticmethod
    def get_score_credito(id_cliente: int) -> float | None:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT score_credito
                FROM cliente
                WHERE id_cliente = %s
            """, (id_cliente,))
            row = cursor.fetchone()
            return row['score_credito'] if row else None

    @staticmethod
    def get_dados_completos_cliente(id_cliente: int) -> dict | None:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT u.nome, u.cpf, u.data_nascimento, u.telefone, u.email, u.tipo_usuario,
                       e.cep, e.local, e.numero_casa, e.bairro, e.cidade, e.estado,
                       c.id_cliente, c.score_credito
                FROM cliente c
                JOIN usuario u ON c.id_usuario = u.id_usuario
                LEFT JOIN endereco e ON u.id_usuario = e.id_usuario
                WHERE c.id_cliente = %s
            """, (id_cliente,))
            return cursor.fetchone()

    @staticmethod
    def list_clientes() -> list[dict]:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT c.id_cliente, u.nome, u.cpf, u.data_nascimento, u.telefone, u.email, c.score_credito
                FROM cliente c
                JOIN usuario u ON c.id_usuario = u.id_usuario
            """)
            return cursor.fetchall()

    @staticmethod
    def update_cliente_score(id_cliente: int, novo_score: float):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE cliente
                SET score_credito = %s
                WHERE id_cliente = %s
            """, (novo_score, id_cliente))

    @staticmethod
    def list_contas_do_cliente(id_cliente: int) -> list[dict]:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT numero_conta, tipo_conta, saldo, status
                FROM conta
                WHERE id_cliente = %s
            """, (id_cliente,))
            return cursor.fetchall()

    @staticmethod
    def delete_cliente(id_cliente: int):
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
