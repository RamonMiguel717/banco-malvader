from utils.exceptions import BancoMalvaderError
from tabelas_dao import Tabelas as T,DBContext
from procedures_dao import Procedures
from conexao import obter_conexao

#Funciona
def criar_banco_e_tabelas():


    try:
        criar_banco()
        obter_conexao()
        criar_tabelas


    except BancoMalvaderError as e:
        log_error(e)
#Funciona
def criar_tabelas():
            # Criação de tabelas
        T.create_table_usuario()
        T.create_table_funcionarios()
        T.create_table_cliente()
        T.create_table_endereco()
        T.create_table_agencia()
        T.create_table_conta()
        T.create_table_conta_poupanca()
        T.create_table_conta_corrente()
        T.create_table_conta_investimento()
        T.create_table_transacao()
        T.create_table_auditoria()
        T.create_table_relatorio()


        Procedures.criar_procedure_gerar_otp()
        Procedures.criar_procedure_invalidar_otp()

#Funciona
def criar_banco():
    with DBContext() as (_, cursor):
        cursor.execute("CREATE DATABASE IF NOT EXISTS banco_malvader")
        cursor.execute("USE banco_malvader")
# Funciona
def apagar_banco():
    # Conecta sem selecionar o banco específico
    with DBContext() as (_, cursor):
        cursor.execute("DROP DATABASE IF EXISTS banco_malvader")


def log_error(e):
    print(f"[ERRO] {str(e)}")


