from conexao import DBContext

class ContaRepository:
    @staticmethod
    def insert_conta(numero_conta, id_agencia, saldo, tipo_conta, id_cliente, data_abertura, status):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO conta (numero_conta, id_agencia, saldo, tipo_conta, id_cliente, data_abertura, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (numero_conta, id_agencia, saldo, tipo_conta, id_cliente, data_abertura, status))
            
 
    @staticmethod
    def get_contas_by_cliente(id_cliente):
        with DBContext() as (conn,cursor):
            cursor.execute("""
                SELECT * FROM conta 
                WHERE id_cliente = %s

""",(id_cliente,))
        return cursor.fetchall()


    @staticmethod
    def list_contas():
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM conta")
            return cursor.fetchall()
            

    @staticmethod
    def update_conta(id_conta, saldo, status):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE conta 
                SET saldo = %s, status = %s
                WHERE id_conta = %s
            """, (saldo, status, id_conta))
            

    @staticmethod
    def delete_conta(id_conta):
        with DBContext() as (_, cursor):
            cursor.execute("DELETE FROM conta WHERE id_conta = %s", (id_conta,))
            

class ContaPoupancaRepository:
    @staticmethod
    def insert_conta_poupanca(id_conta, taxa_rendimento, ultimo_rendimento):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO conta_poupanca (id_conta, taxa_rendimento, ultimo_rendimento)
                VALUES (%s, %s, %s)
            """, (id_conta, taxa_rendimento, ultimo_rendimento))
            

    @staticmethod
    def update_conta_poupanca(id_conta_poupanca, taxa_rendimento, ultimo_rendimento):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE conta_poupanca
                SET taxa_rendimento = %s, ultimo_rendimento = %s
                WHERE id_conta_poupanca = %s
            """, (taxa_rendimento, ultimo_rendimento, id_conta_poupanca))
            

class ContaCorrenteRepository:
    @staticmethod
    def insert_conta_corrente(id_conta, limite, data_vencimento, taxa_manutencao):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO conta_corrente (id_conta, limite, data_vencimento, taxa_manutencao)
                VALUES (%s, %s, %s, %s)
            """, (id_conta, limite, data_vencimento, taxa_manutencao))
            

    @staticmethod
    def update_conta_corrente(id_conta_corrente, limite, data_vencimento, taxa_manutencao):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE conta_corrente
                SET limite = %s, data_vencimento = %s, taxa_manutencao = %s
                WHERE id_conta_corrente = %s
            """, (limite, data_vencimento, taxa_manutencao, id_conta_corrente))
            

class ContaInvestimentoRepository:
    @staticmethod
    def insert_conta_investimento(id_conta, perfil_risco, valor_minimo, taxa_rendimento_base):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO conta_investimentos (id_conta, perfil_risco, valor_minimo, taxa_rendimento_base)
                VALUES (%s, %s, %s, %s)
            """, (id_conta, perfil_risco, valor_minimo, taxa_rendimento_base))
            

    @staticmethod
    def update_conta_investimento(id_conta_investimento, perfil_risco, valor_minimo, taxa_rendimento_base):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE conta_investimentos
                SET perfil_risco = %s, valor_minimo = %s, taxa_rendimento_base = %s
                WHERE id_conta_investimento = %s
            """, (perfil_risco, valor_minimo, taxa_rendimento_base, id_conta_investimento))
            

class TransacaoRepository:
    @staticmethod
    def insert_transacao(id_conta_origem, id_conta_destino, tipo_transacao, valor, data_hora, descricao):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO transacao (id_conta_origem, id_conta_destino, tipo_transacao, valor, data_hora, descricao)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_conta_origem, id_conta_destino, tipo_transacao, valor, data_hora, descricao))
            