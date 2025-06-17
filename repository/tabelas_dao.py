"""
TabelasDao é a criação de todas as tabelas a serem utilizadas no banco de dados, trabalha por meio de uma chamada de "Cursor"
que basicamente é uma emulação de chamadas SQL por meio de Python (não se preocupe com isso)

DBContext retorna 2 argumentos:
    - Comment (inutilizado, foi substituído por " _ ")
    - Cursor -> O que você utilizará para fazer chamadas SQL e manipulações no banco de dados.

Além da criação das tabelas, também criei os Triggers em uma classe própria chamada Procedures
não é a melhor das organizações mas é o que funciona no momento, pode tomar a liberdade de organizar da maneira que achar melhor
só garanta que refatorou o codigo,
"""
from conexao import DBContext

class Tabelas:
    # Funciona
    def create_table_usuario():
        with DBContext() as (_, cursor):
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
                    nome VARCHAR(100) NOT NULL,
                    cpf VARCHAR(11) NOT NULL UNIQUE,
                    data_nascimento DATE NOT NULL,
                    telefone VARCHAR(15),
                    email VARCHAR(50),
                    tipo_usuario ENUM('FUNCIONARIO', 'CLIENTE') NOT NULL,
                    senha_hash VARCHAR(255),
                    otp_codigo VARCHAR(6),
                    otp_ativo BOOLEAN DEFAULT FALSE,
                    otp_expiracao DATETIME
                );
            """)
    # Funciona
    def create_table_funcionarios():
            # Tabela de funcionarios
        with DBContext() as (_, cursor):
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS funcionarios (
                    id_funcionario INT PRIMARY KEY AUTO_INCREMENT,
                    id_usuario INT,
                    codigo_funcionario VARCHAR(50) NOT NULL UNIQUE,
                    cargo VARCHAR(50),
                    id_supervisor INT,
                    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
                    FOREIGN KEY (id_supervisor) REFERENCES funcionarios(id_funcionario)
                );
            """)
    # Funciona
    def create_table_cliente():
            # Tabela de clientes
        with DBContext() as (_, cursor):
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cliente (
                    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
                    id_usuario INT,
                    score_credito DECIMAL(5,2) DEFAULT 0,
                    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
                );
            """)
    # Funciona
    def create_table_endereco():
            # Tabela de enderecos
        with DBContext() as (_, cursor):
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
                    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
                );
            """)
    # Funciona
    def create_table_agencia():
            # Tabela de agencias
        with DBContext() as (_, cursor):
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agencia (
                    id_agencia INT PRIMARY KEY AUTO_INCREMENT,
                    nome VARCHAR(100) NOT NULL,
                    codigo_agencia VARCHAR(50) NOT NULL UNIQUE,
                    endereco_id INT,
                    FOREIGN KEY (endereco_id) REFERENCES endereco(id_endereco)
                );
            """)
    # Funciona
    @staticmethod
    def create_table_conta():
            # Tabela de contas
        with DBContext() as (_, cursor):
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
    # Funciona
    @staticmethod
    def create_table_conta_poupanca():
        with DBContext() as (_, cursor):
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conta_poupanca (
                    id_conta INT PRIMARY KEY,
                    taxa_rendimento DECIMAL(5, 2),
                    ultimo_rendimento DATE,
                    FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
                );
            """)

    # Funciona      
    @staticmethod
    def create_table_conta_corrente():
        with DBContext() as (_, cursor):
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conta_corrente (
                    id_conta INT PRIMARY KEY,
                    limite DECIMAL(10, 2),
                    data_vencimento DATE,
                    taxa_manutencao DECIMAL(5, 2),
                    FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
                );
            """)
    # Funciona
    @staticmethod
    def create_table_conta_investimento():
        with DBContext() as (_, cursor):
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conta_investimento (
                    id_conta INT PRIMARY KEY,
                    perfil_risco VARCHAR(50),
                    valor_minimo DECIMAL(10, 2),
                    taxa_rendimento_base DECIMAL(5, 2),
                    FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
                );
            """)

    # Funciona
    @staticmethod
    def create_table_transacao():
            # Transações
        with DBContext() as (_, cursor):
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
# Funciona 
    @staticmethod 
    def create_table_auditoria():
            # Auditoria
        with DBContext() as (_, cursor):
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS auditoria (
                    id_auditoria INT PRIMARY KEY AUTO_INCREMENT,
                    id_usuario INT,
                    acao VARCHAR(255),
                    data_hora DATETIME,
                    detalhes TEXT,
                    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
                );
            """)
# Funciona
    @staticmethod
    def create_table_relatorio():
            # Relatório
        with DBContext() as (_, cursor):
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
# Funciona
@staticmethod
def apagar_tabelas():
    with DBContext() as (_, cursor):
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        tabelas = [
            "transacao",
            "conta_corrente",
            "conta_poupanca",
            "conta_investimento",
            "conta",
            "cliente",
            "funcionario",
            "agencia",
            "usuarios",
            "endereco",
            "auditoria"
        ]

        for tabela in tabelas:
            cursor.execute(f"DROP TABLE IF EXISTS {tabela};")

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")


class procedures:
 
    @staticmethod
    def criar_trigger_validar_senha():
        sql = """
        DROP TRIGGER IF EXISTS validar_senha;

        CREATE TRIGGER validar_senha
        BEFORE UPDATE ON usuario
        FOR EACH ROW
        BEGIN
            IF NEW.senha_hash REGEXP '^[0-9a-f]{32}$' THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Senha deve ser atualizada via procedure com validação';
            END IF;
        END;
        """
        with DBContext() as (_, cursor):
            for statement in sql.strip().split(';'):
                if statement.strip():
                    cursor.execute(statement + ';')

    @staticmethod
    def gerar_otp():
        sql = """
        DROP PROCEDURE IF EXISTS gerar_otp;
        CREATE PROCEDURE gerar_otp(IN id_usuario INT)
        BEGIN
            DECLARE novo_otp VARCHAR(6);
            SET novo_otp = LPAD(FLOOR(RAND() * 1000000), 6, '0');
            UPDATE usuario
            SET
                otp_codigo = novo_otp,
                otp_ativo = TRUE,
                otp_expiracao = NOW() + INTERVAL 5 MINUTE
            WHERE id_usuario = id_usuario;
            SELECT novo_otp AS otp;
        END;
        """
        with DBContext() as (_, cursor):
            for statement in sql.strip().split(';'):
                if statement.strip():
                    cursor.execute(statement + ';')

    @staticmethod
    def invalidar_otp():
        sql = """
        DROP PROCEDURE IF EXISTS invalidar_otp;
        CREATE PROCEDURE invalidar_otp(IN id_usuario INT)
        BEGIN
            UPDATE usuario
            SET
                otp_codigo = NULL,
                otp_ativo = FALSE,
                otp_expiracao = NULL
            WHERE id_usuario = id_usuario;
        END;
        """
        with DBContext() as (_, cursor):
            for statement in sql.strip().split(';'):
                if statement.strip():
                    cursor.execute(statement + ';')

    #TODO criar um procedure para calcular o SCORE DE CRÉDITO

        