from banco_malvader.model.conta_model import Conta
from banco_malvader.model.conta_poupanca_model import ContaPoupanca
from banco_malvader.model.conta_corrente_model import ContaCorrente
from banco_malvader.model.conta_investimento_model import ContaInvestimento
from banco_malvader.model.transacao_model import Transacao
from banco_malvader.conexao import DBContext


"""
Dentro deste documento existem TODAS as classes de CONTAS (conta poupança, investimento...)
Estão declaradas em suas respectivas classes, entretanto há uma classe base dentro de ContaRepository 
Não confunda, não são a mesma coisa.

"""


class ContaRepository:
    @staticmethod
    def insert(conta: Conta):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO conta (numero_conta, id_agencia, saldo, tipo_conta, id_cliente, data_abertura, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                conta.numero_conta, conta.id_agencia, conta.saldo,
                conta.tipo_conta, conta.id_cliente, conta.data_abertura, conta.status
            ))

    @staticmethod
    def get_contas_by_cliente(id_cliente) -> list[Conta]:
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM conta WHERE id_cliente = %s", (id_cliente,))
            rows = cursor.fetchall()
            return [Conta(**row) for row in rows]

    @staticmethod
    def get_conta_by_id(id_conta) -> Conta | None:
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM conta WHERE id_conta = %s", (id_conta,))
            row = cursor.fetchone()
            return Conta(**row) if row else None

    @staticmethod
    def list_contas() -> list[Conta]:
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM conta")
            rows = cursor.fetchall()
            return [Conta(**row) for row in rows]

    @staticmethod
    def update_conta(id_conta, saldo, status):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE conta SET saldo = %s, status = %s WHERE id_conta = %s
            """, (saldo, status, id_conta))

    @staticmethod
    def atualizar_saldo(id_conta, saldo):
        with DBContext() as (_, cursor):
            cursor.execute("UPDATE conta SET saldo = %s WHERE id_conta = %s", (saldo, id_conta))

    @staticmethod
    def delete_conta(id_conta):
        with DBContext() as (_, cursor):
            cursor.execute("DELETE FROM conta WHERE id_conta = %s", (id_conta,))

    @staticmethod
    def encerrar_conta(id_conta):
        with DBContext() as (_, cursor):
            cursor.execute("UPDATE conta SET status = 'ENCERRADA' WHERE id_conta = %s", (id_conta,))


 
class ContaPoupancaRepository:
    @staticmethod
    def insert(conta: ContaPoupanca):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO conta_poupanca (id_conta, taxa_rendimento, ultimo_rendimento)
                VALUES (%s, %s, %s)
            """, (conta.id_conta, conta.taxa_rendimento, conta.ultimo_rendimento))

    @staticmethod
    def update(conta: ContaPoupanca):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE conta_poupanca SET taxa_rendimento = %s, ultimo_rendimento = %s
                WHERE id_conta = %s
            """, (conta.taxa_rendimento, conta.ultimo_rendimento, conta.id_conta))

    @staticmethod
    def get_by_id(id_conta) -> ContaPoupanca | None:
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM conta_poupanca WHERE id_conta = %s", (id_conta,))
            row = cursor.fetchone()
            return ContaPoupanca(**row) if row else None

    @staticmethod
    def get_by_id_cliente(id_cliente) -> ContaPoupanca | None:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT cp.*
                FROM conta_poupanca cp
                JOIN conta c ON cp.id_conta = c.id_conta
                WHERE c.id_cliente = %s
            """, (id_cliente,))
            row = cursor.fetchone()
            return ContaPoupanca(**row) if row else None

    @staticmethod
    def projetar_rendimento(id_conta: int) -> float:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT c.saldo, cp.taxa_rendimento
                FROM conta c
                JOIN conta_poupanca cp ON c.id_conta = cp.id_conta
                WHERE c.id_conta = %s
            """, (id_conta,))
            dados = cursor.fetchone()
            if not dados:
                return 0.0
            return round(dados["saldo"] * (dados["taxa_rendimento"] / 100), 2)
        
class ContaCorrenteRepository:
    @staticmethod
    def insert(conta: ContaCorrente):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO conta_corrente (id_conta, limite, data_vencimento, taxa_manutencao)
                VALUES (%s, %s, %s, %s)
            """, (conta.id_conta, conta.limite, conta.data_vencimento, conta.taxa_manutencao))

    @staticmethod
    def update(conta: ContaCorrente):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE conta_corrente SET limite = %s, data_vencimento = %s, taxa_manutencao = %s
                WHERE id_conta = %s
            """, (conta.limite, conta.data_vencimento, conta.taxa_manutencao, conta.id_conta))

    @staticmethod
    def get_by_id(id_conta) -> ContaCorrente | None:
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM conta_corrente WHERE id_conta = %s", (id_conta,))
            row = cursor.fetchone()
            return ContaCorrente(**row) if row else None

    @staticmethod
    def get_by_id_cliente(id_cliente) -> ContaCorrente | None:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT cc.*
                FROM conta_corrente cc
                JOIN conta c ON cc.id_conta = c.id_conta
                WHERE c.id_cliente = %s
            """, (id_cliente,))
            row = cursor.fetchone()
            return ContaCorrente(**row) if row else None
class ContaInvestimentoRepository:
    @staticmethod
    def insert(conta: ContaInvestimento):
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO conta_investimento (id_conta, perfil_risco, valor_minimo, taxa_rendimento_base)
                VALUES (%s, %s, %s, %s)
            """, (conta.id_conta, conta.perfil_risco, conta.valor_minimo, conta.taxa_rendimento_base))

    @staticmethod
    def update(conta: ContaInvestimento):
        with DBContext() as (_, cursor):
            cursor.execute("""
                UPDATE conta_investimento
                SET perfil_risco = %s, valor_minimo = %s, taxa_rendimento_base = %s
                WHERE id_conta = %s
            """, (conta.perfil_risco, conta.valor_minimo, conta.taxa_rendimento_base, conta.id_conta))

    @staticmethod
    def get_by_id(id_conta) -> ContaInvestimento | None:
        with DBContext() as (_, cursor):
            cursor.execute("SELECT * FROM conta_investimento WHERE id_conta = %s", (id_conta,))
            row = cursor.fetchone()
            return ContaInvestimento(**row) if row else None

    @staticmethod
    def get_by_id_cliente(id_cliente) -> ContaInvestimento | None:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT ci.*
                FROM conta_investimento ci
                JOIN conta c ON ci.id_conta = c.id_conta
                WHERE c.id_cliente = %s
            """, (id_cliente,))
            row = cursor.fetchone()
            return ContaInvestimento(**row) if row else None

    @staticmethod
    def projetar_rendimento(id_conta: int) -> float:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT c.saldo, ci.taxa_rendimento_base, ci.perfil_risco
                FROM conta c
                JOIN conta_investimento ci ON c.id_conta = ci.id_conta
                WHERE c.id_conta = %s
            """, (id_conta,))
            dados = cursor.fetchone()
            if not dados:
                return 0.0

            multiplicador = {
                "BAIXO": 1.0,
                "MEDIO": 1.2,
                "ALTO": 1.5
            }.get(dados["perfil_risco"].upper(), 1.0)

            return round(dados["saldo"] * (dados["taxa_rendimento_base"] / 100) * multiplicador, 2)

class TransacaoRepository:

    @staticmethod
    def insert(transacao: Transacao) -> int:
        with DBContext() as (_, cursor):
            cursor.execute("""
                INSERT INTO transacao (id_conta_origem, id_conta_destino, tipo_transacao, valor, data_hora, descricao)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                transacao.id_conta_origem,
                transacao.id_conta_destino,
                transacao.tipo_transacao,
                transacao.valor,
                transacao.data_hora,
                transacao.descricao
            ))
            return cursor.lastrowid


    @staticmethod
    def get_transacoes_da_conta(id_conta: int, limite: int = 50) -> list[Transacao]:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT *
                FROM transacao
                WHERE id_conta_origem = %s OR id_conta_destino = %s
                ORDER BY data_hora DESC
                LIMIT %s
            """, (id_conta, id_conta, limite))
            rows = cursor.fetchall()
            return [Transacao(**row) for row in rows]

    @staticmethod
    def get_data_ultima_transacao(id_conta: int):
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT MAX(data_hora) as ultima_transacao
                FROM transacao
                WHERE id_conta_origem = %s OR id_conta_destino = %s
            """, (id_conta, id_conta))
            resultado = cursor.fetchone()
            return resultado["ultima_transacao"] if resultado else None

    @staticmethod
    def get_transacoes_por_periodo(id_conta: int, data_inicio, data_fim) -> list[Transacao]:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT *
                FROM transacao
                WHERE (id_conta_origem = %s OR id_conta_destino = %s)
                AND data_hora BETWEEN %s AND %s
                ORDER BY data_hora DESC
            """, (id_conta, id_conta, data_inicio, data_fim))
            rows = cursor.fetchall()
            return [Transacao(**row) for row in rows]

    @staticmethod
    def get_transacoes_por_tipo(id_conta: int, tipo_transacao: str) -> list[Transacao]:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT *
                FROM transacao
                WHERE (id_conta_origem = %s OR id_conta_destino = %s)
                AND tipo_transacao = %s
                ORDER BY data_hora DESC
            """, (id_conta, id_conta, tipo_transacao))
            rows = cursor.fetchall()
            return [Transacao(**row) for row in rows]

    @staticmethod
    def get_total_movimentado_mensal(id_conta: int, ano: int, mes: int) -> float:
        with DBContext() as (_, cursor):
            cursor.execute("""
                SELECT SUM(valor) as total
                FROM transacao
                WHERE (id_conta_origem = %s OR id_conta_destino = %s)
                AND YEAR(data_hora) = %s AND MONTH(data_hora) = %s
            """, (id_conta, id_conta, ano, mes))
            resultado = cursor.fetchone()
            return float(resultado["total"]) if resultado and resultado["total"] else 0.0
