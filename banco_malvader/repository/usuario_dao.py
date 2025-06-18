from banco_malvader.conexao import DBContext
from banco_malvader.repository.auditoria_dao import AuditoriaRepository
from banco_malvader.model.usuario_model import Usuario
from datetime import datetime


class UsuarioRepository:
    """
    Classe responsável por manipular dados da tabela USUARIO.
    """

    @staticmethod
    def insert_usuario(usuario: Usuario):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO usuario (nome, cpf, data_nascimento, telefone, email, tipo_usuario, senha_hash, otp_codigo, otp_ativo, otp_expiracao)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                usuario.nome,
                usuario.cpf,
                usuario.data_nascimento,
                usuario.telefone,
                usuario.email,
                usuario.tipo_usuario,
                usuario.senha,
                usuario.otp_codigo,
                usuario.otp_ativo,
                usuario.otp_expiracao
            ))

    @staticmethod
    def get_usuario_by_id(id_usuario: int) -> Usuario | None:
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
            row = cursor.fetchone()
            return Usuario.from_row(row) if row else None

    @staticmethod
    def get_usuario_by_cpf(cpf: str) -> Usuario | None:
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM usuario WHERE cpf = %s", (cpf,))
            row = cursor.fetchone()
            return Usuario.from_row(row) if row else None

    @staticmethod
    def buscar_por_nome(nome_parcial: str) -> list[Usuario]:
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM usuario WHERE nome LIKE %s", (f"%{nome_parcial}%",))
            rows = cursor.fetchall()
            return [Usuario(**row) for row in rows]

    @staticmethod
    def list_usuario() -> list[Usuario]:
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM usuario")
            rows = cursor.fetchall()
            return [Usuario(**row) for row in rows]

    @staticmethod
    def update_usuario(id_usuario: int, telefone: str = None, email: str = None, senha_hash: str = None):
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

    @staticmethod
    def update_senha(id_usuario: int, nova_senha_hash: str):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE usuario
                SET senha_hash = %s
                WHERE id_usuario = %s
            """, (nova_senha_hash, id_usuario))

    @staticmethod
    def delete_usuario(id_usuario: int):
        with DBContext() as (_, cursor):
            cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))

    @staticmethod
    def gerar_otp(id_usuario: int) -> str | None:
        with DBContext() as (_, cursor):
            cursor.callproc("gerar_otp", [id_usuario])
            for resultado in cursor.stored_results():
                otp = resultado.fetchone()
                return otp['otp'] if otp else None

    @staticmethod
    def validar_otp(id_usuario: int, otp_informado: str) -> bool:
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
    def invalidar_otp(id_usuario: int):
        with DBContext() as (_, cursor):
            cursor.execute("CALL invalidar_otp(%s)", (id_usuario,))

    @staticmethod
    def registrar_login(id_usuario: int, sucesso: bool):
        try:
            detalhes = f'{{"resultado": "{ "SUCESSO" if sucesso else "FALHA" }"}}'
            return AuditoriaRepository.insert_auditoria(id_usuario, "LOGIN", detalhes)
        except Exception as e:
            raise Exception(f"Erro ao registrar login na auditoria: {e}")

    @staticmethod
    def tentativas_recentes_falhas(id_usuario: int) -> int:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT COUNT(*) AS falhas
                FROM auditoria
                WHERE id_usuario = %s AND acao = 'LOGIN'
                  AND JSON_EXTRACT(detalhes, '$.resultado') = 'FALHA'
                  AND data_hora >= NOW() - INTERVAL 10 MINUTE
            """, (id_usuario,))
            return cursor.fetchone()['falhas']
