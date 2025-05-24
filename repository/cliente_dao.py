import mysql.connector
from repository.conexao import obter_conexao
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

load_dotenv()

class DBContext:
      def __enter__(self):
            self.conn = obter_conexao()
            self.cursor = self.conn.cursor()
            return self.conn,self.cursor
      
      def __exit__(self,exc_type,exc_value,traceback):
            if exc_type:
                  print("Erro no banco",exc_value)
                  self.conn.rollback()
            else:
                  self.conn.commit()
            self.conn.close()
        


def criar_banco_e_tabelas():
    try:
            create_table_usuarios()
            create_table_funcionarios()
            create_table_cliente()
            create_table_endereco()
            create_table_agencia()
            create_table_conta()
            create_table_cotnta_poupanca()
            create_table_conta_corrente()
            create_table_conta_investimentos()
            create_table_transacao()
            create_table_auditoria()
            create_table_relatorio()

    except mysql.connector.Error as err:
        tratar_erro_mysql(err)


def criar_banco():
    with DBContext as (conn,cursor):
        cursor.execute("CREATE DATABASE IF NOT EXISTS banco_malvader")
        cursor.execute("USE banco_malvader")

def create_table_usuarios():
        # Tabela de usuarios
     with DBContext as (conn,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(100) NOT NULL,
                cpf VARCHAR(11) NOT NULL UNIQUE,
                data_nascimento DATE NOT NULL,
                telefone VARCHAR(15),
                tipo_usuario VARCHAR(50),
                senha_hash VARCHAR(255),
                otp_ativo BOOLEAN DEFAULT FALSE,
                otp_expiracao DATETIME
            );
        """)
def create_table_funcionarios():
        # Tabela de funcionarios
    with DBContext as (conn,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS funcionarios (
                id_funcionario INT PRIMARY KEY AUTO_INCREMENT,
                id_usuario INT,
                codigo_funcionario VARCHAR(50) NOT NULL UNIQUE,
                cargo VARCHAR(50),
                id_supervisor INT,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
                FOREIGN KEY (id_supervisor) REFERENCES funcionarios(id_funcionario)
            );
        """)
def create_table_cliente():
        # Tabela de clientes
    with DBContext as (conn,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cliente (
                id_cliente INT PRIMARY KEY AUTO_INCREMENT,
                id_usuario INT,
                score_credito INT,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
            );
        """)
def create_table_endereco():
        # Tabela de enderecos
    with DBContext as (conn,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS endereco (
                id_endereco INT PRIMARY KEY AUTO_INCREMENT,
                id_usuario INT,
                cep VARCHAR(10) NOT NULL,
                local VARCHAR(100) NOT NULL,
                numero_casa VARCHAR(10) NOT NULL,
                bairro VARCHAR(100) NOT NULL,
                cidade VARCHAR(100) NOT NULL,
                estado VARCHAR(100) NOT NULL,
                complemento VARCHAR(100),
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
            );
        """)
def create_table_agencia():
        # Tabela de agencias
    with DBContext as (conn,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agencia (
                id_agencia INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(100) NOT NULL,
                codigo_agencia VARCHAR(50) NOT NULL UNIQUE,
                endereco_id INT,
                FOREIGN KEY (endereco_id) REFERENCES endereco(id_endereco)
            );
        """)
def create_table_conta():
        # Tabela de contas
    with DBContext as (conn,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conta (
                id_conta INT PRIMARY KEY AUTO_INCREMENT,
                numero_conta VARCHAR(20) NOT NULL UNIQUE,
                id_agencia INT,
                saldo DECIMAL(10, 2),
                tipo_conta VARCHAR(50),
                id_cliente INT,
                data_abertura DATE,
                status VARCHAR(50),
                FOREIGN KEY (id_agencia) REFERENCES agencia(id_agencia),
                FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
            );
        """)
def create_table_cotnta_poupanca():
        # Conta poupança
    with DBContext as (conn,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conta_poupanca (
                id_conta_poupanca INT PRIMARY KEY AUTO_INCREMENT,
                id_conta INT UNIQUE,
                taxa_rendimento DECIMAL(5, 2),
                ultimo_rendimento DATE,
                FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
            );
        """)
def create_table_conta_corrente():
        # Conta corrente
    with DBContext as (conn,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conta_corrente (
                id_conta_corrente INT PRIMARY KEY AUTO_INCREMENT,
                id_conta INT UNIQUE,
                limite DECIMAL(10, 2),
                data_vencimento DATE,
                taxa_manutencao DECIMAL(5, 2),
                FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
            );
        """)
def create_table_conta_investimentos():
        # Conta investimento
    with DBContext as (conn,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conta_investimentos (
                id_conta_investimento INT PRIMARY KEY AUTO_INCREMENT,
                id_conta INT UNIQUE,
                perfil_risco VARCHAR(50),
                valor_minimo DECIMAL(10, 2),
                taxa_rendimento_base DECIMAL(5, 2),
                FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
            );
        """)
def create_table_transacao():
        # Transações
    with DBContext as (conn,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transacao (
                id_transacao INT PRIMARY KEY AUTO_INCREMENT,
                id_conta_origem INT,
                id_conta_destino INT,
                tipo_transacao VARCHAR(50),
                valor DECIMAL(10, 2),
                data_hora DATETIME,
                descricao TEXT,
                FOREIGN KEY (id_conta_origem) REFERENCES conta(id_conta),
                FOREIGN KEY (id_conta_destino) REFERENCES conta(id_conta)
            );
        """)
def create_table_auditoria():
        # Auditoria
    with DBContext as (conn,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS auditoria (
                id_auditoria INT PRIMARY KEY AUTO_INCREMENT,
                id_usuario INT,
                acao VARCHAR(255),
                data_hora DATETIME,
                detalhes TEXT,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
            );
        """)
def create_table_relatorio():
        # Relatório
    with DBContext as (conn,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS relatorio (
                id_relatorio INT PRIMARY KEY AUTO_INCREMENT,
                id_funcionario INT,
                tipo_relatorio VARCHAR(100),
                data_geracao DATE,
                conteudo TEXT,
                FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario)
            );
        """)
    
  

def tratar_erro_mysql(err):
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Erro de acesso: usuário ou senha incorretos")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Banco de dados não existe e não pode ser criado.")
    else:
        print(f"Erro ao se conectar: {err}")

def insert_cliente(id_usuario,score_credito):
    with DBContext as (conn,cursor):
        cursor.execute("""
        INSERT INTO cliente (id_usuario,score_credito) VALUES (%s,%s)
    """,(id_usuario,score_credito))
 

def listar_clientes():
    with DBContext as (conn,cursor):

        cursor.execute["SELECT * FROM cliente"]
        clintes = cursor.fetchall()


def atualizar_cliente(id_cliente,novo_score):
    with DBContext as (conn,cursor):

      cursor.execute("""
        UPDATE cliente SET score_credito = %s WHERE id_cliente = %s
""",(novo_score,id_cliente))
    
    
def deletar_cliente(id_cliente):
    with DBContext as (conn,cursor):

      cursor.execute["DELETE FROM cliente WHERE id_cliente = %s",(id_cliente)]