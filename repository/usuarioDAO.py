from conexao import DBContext
from utils import auxiliares


@staticmethod
def insert_usuario(nome, cpf, data_nascimento, telefone,email, tipo_usuario, senha_hash, otp_ativo=False, otp_expiracao=None):
    with DBContext() as (_, cursor):
        cursor.execute("""
            INSERT INTO usuarios (nome, cpf, data_nascimento, telefone,email, tipo_usuario, senha_hash, otp_ativo, otp_expiracao)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (nome, cpf, data_nascimento, telefone,email, tipo_usuario, senha_hash, otp_ativo, otp_expiracao))

@staticmethod
def get_usuario_by_id(id_usuario):
    with DBContext() as (_, cursor):
        cursor.execute("""
            SELECT * FROM usuario
            WHERE id_usuario = %s
        """, (id_usuario,))
        return cursor.fetchone()

@staticmethod
def get_usuario_by_cpf(cpf):
    with DBContext() as (_, cursor):
        cursor.execute("""
            SELECT * FROM usuario
            WHERE id_cliente = %s
        """, (cpf,))
        resultado = cursor.fetchone()
    return resultado  

@staticmethod
def list_usuarios():
    with DBContext() as (_, cursor):
        cursor.execute("SELECT * FROM usuarios")
        return cursor.fetchall()
        

@staticmethod
def update_usuario(id_usuario, nome, telefone, tipo_usuario):
    with DBContext() as (_, cursor):
        cursor.execute("""
            UPDATE usuarios
            SET nome = %s, telefone = %s, tipo_usuario = %s
            WHERE id_usuario = %s
        """, (nome, telefone, tipo_usuario, id_usuario))

@staticmethod
def delete_usuario(id_usuario):
    with DBContext() as (_, cursor):
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))