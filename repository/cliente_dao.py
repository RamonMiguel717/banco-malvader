import mysql.connector
from repository.conexao import obter_conexao
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
load_dotenv()

def criar_banco_e_tabelas():
    try:
#cria coneça
        con = obter_conexao
        cursor = con.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXIST banco_malvader")
        cursor.execute("USE banco_malvader")

        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'banco_malvader'
              AND table_name = 'usuarios'
        """)

        table_exists = cursor.fetchone()[0]

        if table_exists == 0:
            print("Tabela 'usuarios' não existe, criando...")
            cursor.execute("""
                CREATE TABLE usuarios(
                    nome VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    cpf VARCHAR(11) NOT NULL UNIQUE PRIMARY KEY,
                    data_nascimento DATE NOT NULL     
                                    )
                        """)
            print("Tabela criada com sucesso.")
        else:
            print("Tabela de usuários já existe.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACESS_DENIED_ERROR:
            print("Erro de acesso: usuário ou senha incorretos")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Banco de dados não existe e não pode ser criado.")
        else:
            print(f"Erro ao se conectar {err}")




def buscar_todos_clientes():
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cliente")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

class UserOperations:
    def insert_user(nome,cpf,email,data_nascimento):
        con = obter_conexao

        cursor = con.cursor()
        cursor.execute("""USE banco_malvader""")
        cursor.execute(f"""
            INSERT INTO usuarios (nome,cpf,email,data_nacimento) VALUES ({nome},{cpf},{email},{data_nascimento})
                       """)