from conexao import DBContext

class RelatorioRepository:
    @staticmethod
    def insert_relatorio(id_funcionario, tipo_relatorio, data_geracao, conteudo):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO relatorio (id_funcionario, tipo_relatorio, data_geracao, conteudo)
                VALUES (%s, %s, %s, %s)
            """, (id_funcionario, tipo_relatorio, data_geracao, conteudo))
            