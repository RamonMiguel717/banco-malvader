from .conexao import DBContext
from utils import auxiliares

class FuncionarioRepository:
    @staticmethod
    def insert_funcionarios(id_usuario,codigo_funcionario,cargo,id_supervisor):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO funcionarios (id_usuario, codigo_funcionario,cargo,id_supervisor VALUES (%s,%s,%s))""",(id_usuario,codigo_funcionario,cargo,id_supervisor)
                ) 
                # TODO: Adicionar retorno confirmando a inserção (ex.: id do novo funcionário)

    @staticmethod
    def find_funcionario_id_by_cpf(cpf: str):
        cpf_limpo = auxiliares.limpar_cpf(cpf)
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT f.id_funcionario
                FROM funcionarios f
                JOIN usuario u ON f.id_usuario = u.id_usuario
                WHERE u.cpf = %s
            """, (cpf_limpo,))
        resultado = cursor.fetchone()
        # TODO: Tratar casos onde o CPF não é encontrado (ex.: lançar exceção ou logar)
        return resultado[0] if resultado else None
    
    @staticmethod
    def list_funcionarios():
        with DBContext() as (conn,cursor):
            cursor.execute("SELECT * FROM funcionarios")
            funcionarios = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, linha)) for linha in funcionarios]
    
    @staticmethod
    def atualizar_funcionario(id_funcionario, novo_codigo_funcionario, novo_cargo_id, novo_supervisor):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE funcionario 
                SET codigo_funcionario = %s,
                    cargo_id = %s,
                    supervisor_id = %s
                WHERE id_usuario = %s
            """, (novo_codigo_funcionario, novo_cargo_id, novo_supervisor, id_funcionario))
            # TODO: Verificar se o id_funcionario existe antes de atualizar
            # TODO: Retornar sucesso ou erro da operação
            
    @staticmethod
    def delete_funcionarios(id_funcionario,senha):
        with DBContext() as (conn,cursor):
            cursor.execute("DELETE FROM funcionarios WHERE id_funcionario = %s",(id_funcionario,))
            # TODO: Adicionar confirmação antes de deletar (ex.: checar se tem subordinados)
            # TODO: Retornar mensagem de sucesso ou falha

