from conexao import DBContext
from utils import auxiliares

class EnderecoRepository:
    @staticmethod
    def insert_endereco(id_usuario, cep, local, numero_casa, bairro, cidade, estado, complemento):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO endereco (id_usuario, cep, local, numero_casa, bairro, cidade, estado, complemento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_usuario, cep, local, numero_casa, bairro, cidade, estado, complemento))

    @staticmethod
    def list_enderecos():
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM endereco")
            dados = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, linha)) for linha in dados]

    @staticmethod
    def update_endereco(id_endereco, cep, local, numero_casa, bairro, cidade, estado, complemento):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE endereco SET cep=%s, local=%s, numero_casa=%s, bairro=%s,
                cidade=%s, estado=%s, complemento=%s WHERE id_endereco=%s
            """, (cep, local, numero_casa, bairro, cidade, estado, complemento, id_endereco))

    @staticmethod
    def delete_endereco(id_endereco):
        with DBContext() as (_, cursor):
            cursor.execute("DELETE FROM endereco WHERE id_endereco = %s", (id_endereco,))