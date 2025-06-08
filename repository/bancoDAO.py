import mysql.connector
from repository.conexao import obter_conexao
from mysql.connector import errorcode
from dotenv import load_dotenv
from .conexao import DBContext
from repository.tabelasDAO import Tabelas as T

load_dotenv()

# Função que trata os erros de SQL
def tratar_erro_mysql(err):
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Erro de acesso: usuário ou senha incorretos")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Banco de dados não existe e não pode ser criado.")
    else:
        print(f"Erro ao se conectar: {err}")

def criar_banco():
    with DBContext() as (_, cursor):
        cursor.execute("CREATE DATABASE IF NOT EXISTS banco_malvader")
        cursor.execute("USE banco_malvader")

# Executa tabelasDAO além da criação do próprio banco de dados
# Será utilizado SOMENTE no inicio do projeto
def criar_banco_e_tabelas():
    from repository.tabelasDAO import Tabelas as T
    try:
            criar_banco()
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

    except mysql.connector.Error as err:
        tratar_erro_mysql(err)

# TODO: Criar uma função para apagar tudo do banco de dados

