from conexao import DBContext
from utils import auxiliares
from auditoriaDAO import AuditoriaRepository
from models.usuario import Usuario
from datetime import datetime

"""
Inclui todas as funções de manipulação de USUARIO
"""

class UsuarioRepository:

    @staticmethod
    def insert_usuario(nome, cpf, data_nascimento, telefone, email, tipo_usuario, senha_hash, otp_ativo=False, otp_expiracao=None):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO usuario (nome, cpf, data_nascimento, telefone, email, tipo_usuario, senha_hash, otp_ativo, otp_expiracao)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nome, cpf, data_nascimento, telefone, email, tipo_usuario, senha_hash, otp_ativo, otp_expiracao))

    @staticmethod
    def get_usuario_by_id(id_usuario):
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
            row = cursor.fetchone()
            return Usuario(**row) if row else None
    # Retorna as informações do OBJETO usuário a partir do id inserido

    @staticmethod
    def get_usuario_by_cpf(cpf):
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM usuario WHERE cpf = %s", (cpf,))
            row = cursor.fetchone()
            return Usuario(**row) if row else None

    @staticmethod
    def buscar_por_nome(nome_parcial):
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM usuario WHERE nome LIKE %s", (f"%{nome_parcial}%",))
            rows = cursor.fetchall()
            return [Usuario(**row) for row in rows]
        # Encontra uma lista de informações de usuários com um nome PARECIDO com o inserido

    @staticmethod
    def list_usuario():
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM usuario")
            rows = cursor.fetchall()
            return [Usuario(**row) for row in rows]
    # Lista todas as informações de todos os usuarios cadastrados

    @staticmethod
    def update_usuario(id_usuario, telefone=None, email=None, senha_hash=None):
        campos = []
        valores = []

        if telefone:
            campos.append("telefone = %s")
            valores.append(telefone)
        if email:
            campos.append("email = %s")
            valores.append(email)
        if senha_hash:
            campos.append("senha_hash = %s")
            valores.append(senha_hash)

        if not campos:
            return

        valores.append(id_usuario)
        query = f"UPDATE usuario SET {', '.join(campos)} WHERE id_usuario = %s"

        with DBContext() as (_, cursor):
            cursor.execute(query, tuple(valores))
    # Atualiza as informações de usuário dependendo do parâmetro passado
    # A utilização dessa classe depende de uma DECLARAÇÃO EXPLICITA de qual informação está sendo atualizada

    @staticmethod
    def update_senha(id_usuario, nova_senha_hash):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE usuario
                SET senha_hash = %s
                WHERE id_usuario = %s
            """, (nova_senha_hash, id_usuario))
    # Atualiza unicamente a senha do cliente

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
    # Gera o OTP necessário para o cliente acessar a plataforma

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
    # Valida o OTP, caso seja ativo retorna codigo e atualiza a expiração

    @staticmethod
    def invalidar_otp(id_usuario):
        with DBContext() as (_, cursor):
            cursor.execute("CALL invalidar_otp(%s)", (id_usuario,))

    @staticmethod
    def registrar_login(id_usuario, sucesso: bool):
        try:
            detalhes = f'{{"resultado": "{ "SUCESSO" if sucesso else "FALHA" }"}}'
            return AuditoriaRepository.insert_auditoria(id_usuario, "LOGIN", detalhes)
        except Exception as e:
            raise Exception(f"Erro ao registrar login na auditoria: {e}")


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
    