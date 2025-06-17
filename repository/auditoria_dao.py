from conexao import DBContext
from datetime import datetime
from model.auditoria_model import Auditoria


class AuditoriaRepository:

    @staticmethod
    def insert_auditoria(id_usuario: int, acao: str, detalhes: str) -> Auditoria:
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO auditoria (id_usuario, acao, data_hora, detalhes)
                VALUES (%s, %s, NOW(), %s)
            """, (id_usuario, acao, detalhes))

            cursor.execute("SELECT LAST_INSERT_ID() AS id")
            result = cursor.fetchone()
            id_auditoria = result["id"]

            # Busca o dado recém inserido para garantir consistência
            cursor.execute("""
                SELECT * FROM auditoria WHERE id_auditoria = %s
            """, (id_auditoria,))
            row = cursor.fetchone()

            return Auditoria(**row) if row else None

    @staticmethod
    def get_auditorias_by_usuario(id_usuario: int) -> list[Auditoria]:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT * FROM auditoria
                WHERE id_usuario = %s
                ORDER BY data_hora DESC
            """, (id_usuario,))
            rows = cursor.fetchall()
            return [Auditoria(**row) for row in rows]

    @staticmethod
    def get_auditorias_by_acao(acao: str) -> list[Auditoria]:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT * FROM auditoria
                WHERE acao = %s
                ORDER BY data_hora DESC
            """, (acao,))
            rows = cursor.fetchall()
            return [Auditoria(**row) for row in rows]

    @staticmethod
    def list_auditorias() -> list[Auditoria]:
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM auditoria ORDER BY data_hora DESC")
            rows = cursor.fetchall()
            return [Auditoria(**row) for row in rows]
