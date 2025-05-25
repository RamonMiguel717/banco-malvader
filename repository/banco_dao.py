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
    with DBContext() as (conn, cursor):
        cursor.execute("CREATE DATABASE IF NOT EXISTS banco_malvader")
        cursor.execute("USE banco_malvader")

def create_table_usuarios():
        # Tabela de usuarios
     with DBContext() as (conn, cursor):
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
    with DBContext() as (conn, cursor):
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
    with DBContext() as (conn, cursor):
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
    with DBContext() as (conn, cursor):
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
    with DBContext() as (conn, cursor):
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
    with DBContext() as (conn, cursor):
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
    with DBContext() as (conn, cursor):
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
    with DBContext() as (conn, cursor):
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
    with DBContext() as (conn, cursor):
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
    with DBContext() as (conn, cursor):
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
    with DBContext() as (conn, cursor):
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
    with DBContext() as (conn, cursor):
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

class UsuarioRepository:
    @staticmethod
    def insert_usuario(nome, cpf, data_nascimento, telefone, tipo_usuario, senha_hash, otp_ativo=False, otp_expiracao=None):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                INSERT INTO usuarios (nome, cpf, data_nascimento, telefone, tipo_usuario, senha_hash, otp_ativo, otp_expiracao)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (nome, cpf, data_nascimento, telefone, tipo_usuario, senha_hash, otp_ativo, otp_expiracao))

    @staticmethod
    def list_usuarios():
        with DBContext() as (conn, cursor):
            cursor.execute("SELECT * FROM usuarios")
            dados = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, linha)) for linha in dados]

    @staticmethod
    def update_usuario(id_usuario, nome, telefone, tipo_usuario):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                UPDATE usuarios
                SET nome = %s, telefone = %s, tipo_usuario = %s
                WHERE id_usuario = %s
            """, (nome, telefone, tipo_usuario, id_usuario))

    @staticmethod
    def delete_usuario(id_usuario):
        with DBContext() as (conn, cursor):
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
#CLIENTES
class ClienteRepository:
    @staticmethod
    def insert_cliente(id_usuario,score_credito):
        with DBContext() as (conn, cursor):
            cursor.execute("""
            INSERT INTO cliente (id_usuario,score_credito) VALUES (%s,%s)
        """,(id_usuario,score_credito))
    
    @staticmethod
    def list_clientes():
        with DBContext() as (conn, cursor):
            cursor.execute("SELECT * FROM cliente")
            clientes = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, linha)) for linha in clientes]
    @staticmethod
    def update_cliente(id_cliente,novo_score):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                UPDATE cliente SET score_credito = %s WHERE id_cliente = %s
        """,(novo_score,id_cliente))
        
    @staticmethod    
    def delete_cliente(id_cliente):
        with DBContext() as (conn, cursor):
            cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (id_cliente,))
#FUNCIONARIOS
class FuncionarioRepository:
    @staticmethod
    def insert_funcionarios(id_usuario,codigo_funcionario,cargo,id_supervisor):
        with DBContext() as (conn,cursor):
            cursor.execute("""
                INSERT INTO funcionarios (id_usuario, codigo_funcionario,cargo,id_supervisor VALUES (%s,%s,%s))""",(id_usuario,codigo_funcionario,cargo,id_supervisor)
                )
    @staticmethod
    def list_funcionarios():
        with DBContext() as (conn,cursor):
            cursor.execute("SELECT * FROM funcionarios")
            funcionarios = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, linha)) for linha in funcionarios]
        
    @staticmethod
    def atualizar_funcionario(id_funcionario, novo_codigo_funcionario, novo_cargo_id, novo_supervisor):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                UPDATE funcionario 
                SET codigo_funcionario = %s,
                    cargo_id = %s,
                    supervisor_id = %s
                WHERE id_usuario = %s
            """, (novo_codigo_funcionario, novo_cargo_id, novo_supervisor, id_funcionario))
            conn.commit()
    @staticmethod
    def delete_funcionarios(id_funcionario,senha):
        with DBContext() as (conn,cursor):
            cursor.execute("DELETE FROM funcionarios WHERE id_funcionario = %s",(id_funcionario))

class EnderecoRepository:
    @staticmethod
    def insert_endereco(id_usuario, cep, local, numero_casa, bairro, cidade, estado, complemento):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                INSERT INTO endereco (id_usuario, cep, local, numero_casa, bairro, cidade, estado, complemento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_usuario, cep, local, numero_casa, bairro, cidade, estado, complemento))

    @staticmethod
    def list_enderecos():
        with DBContext() as (conn, cursor):
            cursor.execute("SELECT * FROM endereco")
            dados = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, linha)) for linha in dados]

    @staticmethod
    def update_endereco(id_endereco, cep, local, numero_casa, bairro, cidade, estado, complemento):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                UPDATE endereco SET cep=%s, local=%s, numero_casa=%s, bairro=%s,
                cidade=%s, estado=%s, complemento=%s WHERE id_endereco=%s
            """, (cep, local, numero_casa, bairro, cidade, estado, complemento, id_endereco))

    @staticmethod
    def delete_endereco(id_endereco):
        with DBContext() as (conn, cursor):
            cursor.execute("DELETE FROM endereco WHERE id_endereco = %s", (id_endereco,))

class AgenciaRepository:
    @staticmethod
    def insert_agencia(nome, codigo_agencia, endereco_id):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                INSERT INTO agencia (nome, codigo_agencia, endereco_id)
                VALUES (%s, %s, %s)
            """, (nome, codigo_agencia, endereco_id))
            conn.commit()

    @staticmethod
    def list_agencias():
        with DBContext() as (conn, cursor):
            cursor.execute("SELECT * FROM agencia")
            agencias = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, linha)) for linha in agencias]

    @staticmethod
    def update_agencia(id_agencia, nome, codigo_agencia):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                UPDATE agencia 
                SET nome = %s, codigo_agencia = %s
                WHERE id_agencia = %s
            """, (nome, codigo_agencia, id_agencia))
            conn.commit()

    @staticmethod
    def delete_agencia(id_agencia):
        with DBContext() as (conn, cursor):
            cursor.execute("DELETE FROM agencia WHERE id_agencia = %s", (id_agencia,))
            conn.commit()

class ContaRepository:
    @staticmethod
    def insert_conta(numero_conta, id_agencia, saldo, tipo_conta, id_cliente, data_abertura, status):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                INSERT INTO conta (numero_conta, id_agencia, saldo, tipo_conta, id_cliente, data_abertura, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (numero_conta, id_agencia, saldo, tipo_conta, id_cliente, data_abertura, status))
            conn.commit()

    @staticmethod
    def list_contas():
        with DBContext() as (conn, cursor):
            cursor.execute("SELECT * FROM conta")
            contas = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, linha)) for linha in contas]

    @staticmethod
    def update_conta(id_conta, saldo, status):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                UPDATE conta 
                SET saldo = %s, status = %s
                WHERE id_conta = %s
            """, (saldo, status, id_conta))
            conn.commit()

    @staticmethod
    def delete_conta(id_conta):
        with DBContext() as (conn, cursor):
            cursor.execute("DELETE FROM conta WHERE id_conta = %s", (id_conta,))
            conn.commit()

class ContaPoupancaRepository:
    @staticmethod
    def insert_conta_poupanca(id_conta, taxa_rendimento, ultimo_rendimento):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                INSERT INTO conta_poupanca (id_conta, taxa_rendimento, ultimo_rendimento)
                VALUES (%s, %s, %s)
            """, (id_conta, taxa_rendimento, ultimo_rendimento))
            conn.commit()

    @staticmethod
    def update_conta_poupanca(id_conta_poupanca, taxa_rendimento, ultimo_rendimento):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                UPDATE conta_poupanca
                SET taxa_rendimento = %s, ultimo_rendimento = %s
                WHERE id_conta_poupanca = %s
            """, (taxa_rendimento, ultimo_rendimento, id_conta_poupanca))
            conn.commit()

class ContaCorrenteRepository:
    @staticmethod
    def insert_conta_corrente(id_conta, limite, data_vencimento, taxa_manutencao):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                INSERT INTO conta_corrente (id_conta, limite, data_vencimento, taxa_manutencao)
                VALUES (%s, %s, %s, %s)
            """, (id_conta, limite, data_vencimento, taxa_manutencao))
            conn.commit()

    @staticmethod
    def update_conta_corrente(id_conta_corrente, limite, data_vencimento, taxa_manutencao):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                UPDATE conta_corrente
                SET limite = %s, data_vencimento = %s, taxa_manutencao = %s
                WHERE id_conta_corrente = %s
            """, (limite, data_vencimento, taxa_manutencao, id_conta_corrente))
            conn.commit()

class ContaInvestimentoRepository:
    @staticmethod
    def insert_conta_investimento(id_conta, perfil_risco, valor_minimo, taxa_rendimento_base):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                INSERT INTO conta_investimentos (id_conta, perfil_risco, valor_minimo, taxa_rendimento_base)
                VALUES (%s, %s, %s, %s)
            """, (id_conta, perfil_risco, valor_minimo, taxa_rendimento_base))
            conn.commit()

    @staticmethod
    def update_conta_investimento(id_conta_investimento, perfil_risco, valor_minimo, taxa_rendimento_base):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                UPDATE conta_investimentos
                SET perfil_risco = %s, valor_minimo = %s, taxa_rendimento_base = %s
                WHERE id_conta_investimento = %s
            """, (perfil_risco, valor_minimo, taxa_rendimento_base, id_conta_investimento))
            conn.commit()

class TransacaoRepository:
    @staticmethod
    def insert_transacao(id_conta_origem, id_conta_destino, tipo_transacao, valor, data_hora, descricao):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                INSERT INTO transacao (id_conta_origem, id_conta_destino, tipo_transacao, valor, data_hora, descricao)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_conta_origem, id_conta_destino, tipo_transacao, valor, data_hora, descricao))
            conn.commit()

class AuditoriaRepository:
    @staticmethod
    def insert_auditoria(id_usuario, acao, data_hora, detalhes):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                INSERT INTO auditoria (id_usuario, acao, data_hora, detalhes)
                VALUES (%s, %s, %s, %s)
            """, (id_usuario, acao, data_hora, detalhes))
            conn.commit()

class RelatorioRepository:
    @staticmethod
    def insert_relatorio(id_funcionario, tipo_relatorio, data_geracao, conteudo):
        with DBContext() as (conn, cursor):
            cursor.execute("""
                INSERT INTO relatorio (id_funcionario, tipo_relatorio, data_geracao, conteudo)
                VALUES (%s, %s, %s, %s)
            """, (id_funcionario, tipo_relatorio, data_geracao, conteudo))
            conn.commit()