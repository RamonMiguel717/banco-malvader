from repository.conexao import DBContext

class AuditoriaRepository:
    @staticmethod
    def insert_auditoria(id_usuario, acao, data_hora, detalhes):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO auditoria (id_usuario, acao, data_hora, detalhes)
                VALUES (%s, %s, %s, %s)
            """, (id_usuario, acao, data_hora, detalhes))