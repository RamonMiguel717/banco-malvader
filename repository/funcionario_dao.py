from .conexao import DBContext
from ..model.funcionario_model import Funcionario
from ..utils import auxiliares

class FuncionarioRepository:

    @staticmethod
    def insert_funcionario(funcionario: Funcionario):
        codigo = auxiliares.gerador_codigo_funcionario(
            funcionario.id_usuario, funcionario.cargo
        )
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO funcionario (id_usuario, codigo_funcionario, cargo, id_supervisor)
                VALUES (%s, %s, %s, %s)
            """, (
                funcionario.id_usuario,
                codigo,
                funcionario.cargo,
                funcionario.id_supervisor
            ))

    @staticmethod
    def find_funcionario_id_by_cpf(cpf: str) -> int | None:
        cpf_limpo = auxiliares.limpar_cpf(cpf)
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT f.id_funcionario
                FROM funcionario f
                JOIN usuario u ON f.id_usuario = u.id_usuario
                WHERE u.cpf = %s
            """, (cpf_limpo,))
            resultado = cursor.fetchone()
            return resultado['id_funcionario'] if resultado else None

    @staticmethod
    def get_funcionario_by_id(id_usuario: int) -> Funcionario | None:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT * FROM funcionario WHERE id_usuario = %s
            """, (id_usuario,))
            resultado = cursor.fetchone()
            return Funcionario(**resultado) if resultado else None

    @staticmethod
    def list_funcionarios() -> list[Funcionario]:
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM funcionario")
            resultados = cursor.fetchall()
            return [Funcionario(**row) for row in resultados]

    @staticmethod
    def atualizar_funcionario(funcionario: Funcionario):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE funcionario 
                SET codigo_funcionario = %s,
                    cargo = %s,
                    id_supervisor = %s
                WHERE id_funcionario = %s
            """, (
                funcionario.codigo_funcionario,
                funcionario.cargo,
                funcionario.id_supervisor,
                funcionario.id_funcionario
            ))

    @staticmethod
    def delete_funcionario(id_funcionario: int):
        with DBContext() as (_, cursor):
            cursor.execute("DELETE FROM funcionario WHERE id_funcionario = %s", (id_funcionario,))
    