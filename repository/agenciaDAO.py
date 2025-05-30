from conexao import DBContext

class AgenciaRepository:
    @staticmethod
    def insert_agencia(nome, codigo_agencia, endereco_id):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO agencia (nome, codigo_agencia, endereco_id)
                VALUES (%s, %s, %s)
            """, (nome, codigo_agencia, endereco_id))
  
    @staticmethod
    def list_agencias():
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM agencia")
            return cursor.fetchall()
            

    @staticmethod
    def update_agencia(id_agencia, nome, codigo_agencia):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE agencia 
                SET nome = %s, codigo_agencia = %s
                WHERE id_agencia = %s
            """, (nome, codigo_agencia, id_agencia))
       

    @staticmethod
    def delete_agencia(id_agencia):
        with DBContext() as (_, cursor):
            cursor.execute("DELETE FROM agencia WHERE id_agencia = %s", (id_agencia,))

