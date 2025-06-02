from conexao import DBContext
from utils import auxiliares
from datetime import datetime


@staticmethod
def insert_usuario(nome, cpf, data_nascimento, telefone,email, tipo_usuario, senha_hash, otp_ativo=False, otp_expiracao=None):
    with DBContext() as (_, cursor):
        cursor.execute("""
            INSERT INTO usuario (nome, cpf, data_nascimento, telefone,email, tipo_usuario, senha_hash, otp_ativo, otp_expiracao)
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
def buscar_por_nome(nome_parcial):
    with DBContext() as (_, cursor):
        cursor.execute("""
            SELECT * FROM usuario
            WHERE nome LIKE %s
        """, (f"%{nome_parcial}%",))
        return cursor.fetchall()


@staticmethod
def list_usuario():
    with DBContext() as (_, cursor):
        cursor.execute("SELECT * FROM usuario")
        return cursor.fetchall()
        

@staticmethod
def update_usuario(id_usuario, nome, telefone, tipo_usuario):
    with DBContext() as (_, cursor):
        cursor.execute("""
            UPDATE usuario
            SET nome = %s, telefone = %s, tipo_usuario = %s
            WHERE id_usuario = %s
        """, (nome, telefone, tipo_usuario, id_usuario))

@staticmethod
def update_senha(id_usuario,nova_senha_hash):
    with DBContext() as (_,cursor):
        cursor.execute("""
            UPDATE usuario
            SET senha_hash = %s
            WHERE id_usuario = %s
        """, (nova_senha_hash, id_usuario))

@staticmethod
def delete_usuario(id_usuario):
    with DBContext() as (_, cursor):
        cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))

@staticmethod
def gerar_otp(id_usuario):
    with DBContext() as (_, cursor):
        cursor.callproc("gerar_otp", [id_usuario])
        for resultado in cursor.stored_results():
            otp = resultado.fetchone()
            return otp['otp'] if otp else None

@staticmethod
def validar_otp(id_usuario, otp_informado):
    with DBContext() as (_, cursor):
        cursor.execute("""
            SELECT otp_ativo, otp_codigo, otp_expiracao
            FROM usuario
            WHERE id_usuario = %s
        """, (id_usuario,))
        dados = cursor.fetchone()

        if not dados or not dados['otp_ativo']:
            return False

        agora = datetime.now()

        return (
            dados['otp_codigo'] == otp_informado and
            dados['otp_expiracao'] > agora
        )

@staticmethod
def invalidar_otp(id_usuario):
    with DBContext() as (_, cursor):
        cursor.execute("""
            CALL invalidar_otp(%s)
        """, (id_usuario,))


@staticmethod
def registrar_login(id_usuario, sucesso: bool):
    with DBContext() as (_, cursor):
        cursor.execute("""
            INSERT INTO auditoria (id_usuario, acao, data_hora, detalhes)
            VALUES (%s, %s, NOW(), %s)
        """, (
            id_usuario,
            'LOGIN',
            f'{{"resultado": "{ "SUCESSO" if sucesso else "FALHA" }"}}'
        ))

@staticmethod
def tentativas_recentes_falhas(id_usuario):
    with DBContext() as (_, cursor):
        cursor.execute("""
            SELECT COUNT(*) AS falhas
            FROM auditoria
            WHERE id_usuario = %s AND acao = 'LOGIN'
              AND JSON_EXTRACT(detalhes, '$.resultado') = 'FALHA'
              AND data_hora >= NOW() - INTERVAL 10 MINUTE
        """, (id_usuario,))
        return cursor.fetchone()['falhas']
