from conexao import DBContext
from model.endereco_model import Endereco

class EnderecoRepository:

    @staticmethod
    def insert_endereco(endereco: Endereco):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO endereco (
                    id_usuario, cep, local, numero_casa, bairro,
                    cidade, estado, complemento
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                endereco.id_usuario,
                endereco.cep,
                endereco.local,
                endereco.numero_casa,
                endereco.bairro,
                endereco.cidade,
                endereco.estado,
                endereco.complemento
            ))

    @staticmethod
    def list_enderecos() -> list[Endereco]:
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM endereco")
            resultados = cursor.fetchall()
            return [Endereco(**row) for row in resultados]

    @staticmethod
    def update_endereco(endereco: Endereco):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE endereco
                SET cep = %s, local = %s, numero_casa = %s, bairro = %s,
                    cidade = %s, estado = %s, complemento = %s
                WHERE id_endereco = %s
            """, (
                endereco.cep,
                endereco.local,
                endereco.numero_casa,
                endereco.bairro,
                endereco.cidade,
                endereco.estado,
                endereco.complemento,
                endereco.id_endereco
            ))

    @staticmethod
    def delete_endereco(id_endereco: int):
        with DBContext() as (_, cursor):
            cursor.execute("DELETE FROM endereco WHERE id_endereco = %s", (id_endereco,))
