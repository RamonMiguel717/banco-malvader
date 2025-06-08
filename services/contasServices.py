from repository.contasDAO import ContaRepository as Conta,ContaPoupancaRepository as CP,ContaCorrenteRepository as CC,ContaInvestimentoRepository as CI
from repository.clienteDAO import ClienteRepository
from datetime import datetime, timedelta
from dateutil import relativedelta
from utils import auxiliares

class ContaService:
    
    @staticmethod
    def criar_conta_base(id_agencia,tipo_conta,id_cliente):    
        numero_conta = auxiliares.gerar_numero_conta()
        data_abertura = datetime.today().date()
        saldo_inicial = 0.0
        status = "ATIVA"
        Conta.insert_conta(numero_conta, id_agencia, saldo_inicial, tipo_conta, id_cliente, data_abertura, status)
        return numero_conta
    
    @staticmethod
    def criar_conta_poupanca(id_conta,taxa_rendimento):
        ultimo_rendimento = None
        CP.insert_conta_poupanca(id_conta,taxa_rendimento,ultimo_rendimento)

    @staticmethod
    def criar_conta_corrente(id_conta,id_cliente):
        score = ClienteRepository.get_score_credito(id_cliente)
        limite = auxiliares.calcular_limite_por_score(score)

        taxa_manutencao = 10.00
        data_vencimento = datetime.today().date()+ relativedelta(months = 6)
        """
        TODO
        O vencimento de uma conta vem a partir do tempo de inatividade da mesma. Então devo criar uma função aux que
        identifique a data da ultima transação, adicione 6 meses e retorne a data_vencimento 
        """
        CC.insert_conta_corrente(id_conta, limite, data_vencimento, taxa_manutencao)

# TODO inacabado