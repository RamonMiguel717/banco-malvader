from conexao import DBContext
from model.relatorio_model import Relatorio
from datetime import datetime

"""
A criação de um relatório é uma função destinada aos FUNCIONARIOS
Em resumo são as Análises de Rendimento do banco ou dos funcionários, isso vai depender do tipo de funcionário que está 
gerando um novo relatório.

TODO esta classe ainda não está em utilização, e não foi finalizada
"""


class RelatorioRepository:

    @staticmethod
    def insert_relatorio(id_funcionario, tipo_relatorio, conteudo):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO relatorio (id_funcionario, tipo_relatorio, data_geracao, conteudo)
                VALUES (%s, %s, NOW(), %s)
            """, (id_funcionario, tipo_relatorio, conteudo))

            cursor.execute("SELECT LAST_INSERT_ID() AS id")
            result = cursor.fetchone()
            id_relatorio = result["id"]

            return Relatorio(
                id_relatorio=id_relatorio,
                id_funcionario=id_funcionario,
                tipo_relatorio=tipo_relatorio,
                data_geracao=datetime.now(),
                conteudo=conteudo
            )

    @staticmethod
    def get_relatorio_by_id(id_relatorio):
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM relatorio WHERE id_relatorio = %s", (id_relatorio,))
            row = cursor.fetchone()
            return Relatorio(**row) if row else None

    @staticmethod
    def list_relatorios():
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM relatorio ORDER BY data_geracao DESC")
            rows = cursor.fetchall()
            return [Relatorio(**row) for row in rows]

    @staticmethod
    def list_relatorios_por_funcionario(id_funcionario):
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT * FROM relatorio
                WHERE id_funcionario = %s
                ORDER BY data_geracao DESC
            """, (id_funcionario,))
            rows = cursor.fetchall()
            return [Relatorio(**row) for row in rows]
