import mysql.connector
from repository.conexao import obter_conexao
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

load_dotenv()

def criar_banco_e_tabelas():
    try:
        con = obter_conexao()
        cursor = con.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS banco_malvader")
        cursor.execute("USE banco_malvader")

        # Tabela de usuarios
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

        # Tabela de funcionarios
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

        # Tabela de clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cliente (
                id_cliente INT PRIMARY KEY AUTO_INCREMENT,
                id_usuario INT,
                score_credito INT,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
            );
        """)

        # Tabela de enderecos
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

        # Tabela de agencias
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agencia (
                id_agencia INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(100) NOT NULL,
                codigo_agencia VARCHAR(50) NOT NULL UNIQUE,
                endereco_id INT,
                FOREIGN KEY (endereco_id) REFERENCES endereco(id_endereco)
            );
        """)

        # Tabela de contas
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

        # Conta poupança
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conta_poupanca (
                id_conta_poupanca INT PRIMARY KEY AUTO_INCREMENT,
                id_conta INT UNIQUE,
                taxa_rendimento DECIMAL(5, 2),
                ultimo_rendimento DATE,
                FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
            );
        """)

        # Conta corrente
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

        # Conta investimento
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conta_investimento (
                id_conta_investimento INT PRIMARY KEY AUTO_INCREMENT,
                id_conta INT UNIQUE,
                perfil_risco VARCHAR(50),
                valor_minimo DECIMAL(10, 2),
                taxa_rendimento_base DECIMAL(5, 2),
                FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
            );
        """)

        # Transações
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

        # Auditoria
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

        # Relatório
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

        con.commit()
        print("Tabelas criadas com sucesso.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro de acesso: usuário ou senha incorretos")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Banco de dados não existe e não pode ser criado.")
        else:
            print(f"Erro ao se conectar: {err}")
    finally:
        cursor.close()
        con.close()
