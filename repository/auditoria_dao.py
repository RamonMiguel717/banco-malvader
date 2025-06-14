from .conexao import DBContext
from datetime import datetime
from ..model.auditoria_model import Auditoria

class AuditoriaRepository:
    @staticmethod
    # Insere a ação praticada pelo USUARIO dentro da tabela de Auditoria
    def insert_auditoria(id_usuario: int, acao: str, detalhes: str) -> Auditoria:
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO auditoria (id_usuario, acao, data_hora, detalhes)
                VALUES (%s, %s, NOW(), %s)
            """, (id_usuario, acao, detalhes))

            cursor.execute("SELECT LAST_INSERT_ID() AS id")
            result = cursor.fetchone()
            id_auditoria = result["id"]

            return Auditoria(
                id_auditoria=id_auditoria,
                id_usuario=id_usuario,
                acao=acao,
                data_hora=datetime.now(),
                detalhes=detalhes
            )
