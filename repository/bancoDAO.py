from repository.tabelasDAO import Tabelas as T
from repository.proceduresDAO import Procedures 
from utils import exceptions

def criar_banco_e_tabelas():


    try:
        criar_banco()

        # Criação de tabelas
        T.create_table_usuario()
        T.create_table_funcionarios()
        T.create_table_cliente()
        T.create_table_endereco()
        T.create_table_agencia()
        T.create_table_conta()
        T.create_table_conta_poupanca()
        T.create_table_conta_corrente()
        T.create_table_conta_investimentos()
        T.create_table_transacao()
        T.create_table_auditoria()
        T.create_table_relatorio()


        Procedures.criar_procedure_gerar_otp()
        Procedures.criar_procedure_invalidar_otp()




    except exceptions.BancoMalvaderError() as e:
        log_error(e)


from repository.conexao import DBContext

def criar_banco():
    with DBContext() as (_, cursor):
        cursor.execute("CREATE DATABASE IF NOT EXISTS banco_malvader")
        cursor.execute("USE banco_malvader")

def log_error(e):
    print(f"[ERRO] {str(e)}")
