from banco_malvader.repository.contas_dao import (
    ContaRepository as CT,
    ContaPoupancaRepository as CP,
    ContaCorrenteRepository as CC,
    ContaInvestimentoRepository as CI,
    TransacaoRepository as TR
)
from banco_malvader.repository.cliente_dao import ClienteRepository
from banco_malvader.model.conta_corrente_model import ContaCorrente
from banco_malvader.model.conta_poupanca_model import ContaPoupanca
from banco_malvader.model.conta_investimento_model import ContaInvestimento
from banco_malvader.model.conta_model import Conta
from banco_malvader.services.usuario_services import UsuarioServices as usuario
from datetime import datetime
from dateutil import relativedelta
from banco_malvader.utils import auxiliares
from banco_malvader.utils.exceptions import ValidacaoNegocioError


class ContaService:

    @staticmethod
    def criar_conta_base(id_agencia, tipo_conta, id_cliente) -> Conta:
        numero_conta = auxiliares.gerar_numero_conta()
        data_abertura = datetime.today().date()

        conta = Conta(
            id_conta=None,
            numero_conta=numero_conta,
            id_agencia=id_agencia,
            saldo=0.0,
            tipo_conta=tipo_conta,
            id_cliente=id_cliente,
            data_abertura=data_abertura,
            status="ATIVA"
        )

        CT.insert(conta)  # Agora passando objeto Conta diretamente

        # Buscar conta recém-criada pelo número (para obter id_conta)
        contas = CT.get_contas_by_cliente(id_cliente)
        conta_criada = next((c for c in contas if c.numero_conta == numero_conta), None)

        return conta_criada


class ContaCorrenteService:

    @staticmethod
    def criar_conta_corrente(id_agencia, id_cliente):
        conta = ContaService.criar_conta_base(id_agencia, "CORRENTE", id_cliente)

        score = ClienteRepository.get_score_credito(id_cliente)
        limite = auxiliares.calcular_limite_por_score(score)
        taxa_manutencao = 10.00
        data_vencimento = datetime.today().date() + relativedelta.relativedelta(months=6)

        conta_corrente = ContaCorrente(
            id_conta=conta.id_conta,
            limite=limite,
            data_vencimento=data_vencimento,
            taxa_manutencao=taxa_manutencao
        )

        CC.insert(conta_corrente)

        return conta.numero_conta


class ContaPoupancaService:

    @staticmethod
    def criar_conta_poupanca(id_agencia, id_cliente, taxa_rendimento=0.5):
        conta = ContaService.criar_conta_base(id_agencia, "POUPANCA", id_cliente)

        conta_poupanca = ContaPoupanca(
            id_conta=conta.id_conta,
            taxa_rendimento=taxa_rendimento,
            ultimo_rendimento=None
        )

        CP.insert(conta_poupanca)

        return conta.numero_conta


class ContaInvestimentoService:

    @staticmethod
    def criar_conta_investimento(id_agencia, id_cliente, perfil_risco, valor_minimo, taxa_rendimento_base):
        conta = ContaService.criar_conta_base(id_agencia, "INVESTIMENTO", id_cliente)

        conta_investimento = ContaInvestimento(
            id_conta=conta.id_conta,
            perfil_risco=perfil_risco,
            valor_minimo=valor_minimo,
            taxa_rendimento_base=taxa_rendimento_base
        )

        CI.insert(conta_investimento)

        return conta.numero_conta
