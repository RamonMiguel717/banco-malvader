from ..repository.contas_dao import (
    ContaRepository as CT,
    ContaPoupancaRepository as CP,
    ContaCorrenteRepository as CC,
    ContaInvestimentoRepository as CI,
    TransacaoRepository as TR
)
from ..repository.cliente_dao import ClienteRepository
from ..model.conta_corrente_model import ContaCorrente
from ..model.conta_poupanca_model import ContaPoupanca
from ..model.conta_investimento_model import ContaInvestimento
from ..model.conta_model import Conta
from .usuario_services import UsuarioServices as usuario
from datetime import datetime, timedelta
from dateutil import relativedelta
from utils import auxiliares
from utils.exceptions import ValidacaoNegocioError


class ContaService:

    @staticmethod
    def criar_conta_base(id_agencia, tipo_conta, id_cliente):
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
        CT.insert(conta)
        return numero_conta

    @staticmethod
    def consultar_saldo(id_conta, senha, otp, id_usuario):
        if not usuario.validar_senha(id_usuario, senha):
            raise ValidacaoNegocioError("Senha inválida.")
        if not usuario.validar_otp(id_usuario, otp):
            raise ValidacaoNegocioError("OTP inválido ou expirado.")

        conta_info = CT.get_conta_by_id(id_conta)
        saldo = conta_info.saldo
        tipo = conta_info.tipo_conta

        if tipo == "POUPANCA":
            rendimento = CP.projetar_rendimento(id_conta)
        elif tipo == "INVESTIMENTO":
            rendimento = CI.projetar_rendimento(id_conta)
        else:
            rendimento = 0.0

        return {
            "saldo": saldo,
            "projecao_rendimento": rendimento
        }

    @staticmethod
    def consultar_extrato(id_conta: int, limite: int = 50):
        extrato = TR.get_transacoes_da_conta(id_conta, limite)
        return [
            {
                "id_transacao": trans.id_transacao,
                "data_hora": trans.data_hora,
                "tipo_transacao": trans.tipo_transacao,
                "valor": float(trans.valor),
                "descricao": trans.descricao,
                "conta_origem": trans.id_conta_origem,
                "conta_destino": trans.id_conta_destino
            }
            for trans in extrato
        ]

    @staticmethod
    def consultar_extrato_por_periodo(id_conta, data_inicio, data_fim):
        data_inicio = auxiliares.tratar_data(data_inicio)
        data_fim = auxiliares.tratar_data(data_fim)

        extrato = TR.get_transacoes_por_periodo(id_conta, data_inicio, data_fim)
        return [
            {
                "id_transacao": trans.id_transacao,
                "data_hora": trans.data_hora,
                "tipo_transacao": trans.tipo_transacao,
                "valor": float(trans.valor),
                "descricao": trans.descricao,
                "conta_origem": trans.id_conta_origem,
                "conta_destino": trans.id_conta_destino
            }
            for trans in extrato
        ]

    @staticmethod
    def depositar(id_conta: int, valor: float, descricao: str = "Depósito"):
        conta = CT.get_conta_by_id(id_conta)
        if not conta or conta.status != "ATIVA":
            raise ValidacaoNegocioError("Conta inválida ou inativa!")

        if valor <= 0:
            raise ValidacaoNegocioError("Valor do depósito deve ser positivo")

        novo_saldo = conta.saldo + valor
        CT.atualizar_saldo(id_conta, novo_saldo)

        TR.insert_transacao(
            id_conta_origem=None,
            id_conta_destino=id_conta,
            tipo_transacao="DEPOSITO",
            valor=valor,
            data_hora=datetime.now(),
            descricao=descricao
        )

        return {"sucesso": True, "novo_saldo": novo_saldo}

    @staticmethod
    def transferir(id_conta_origem: int, id_conta_destino: int, valor: float, descricao: str = "Transferência"):
        origem = CT.get_conta_by_id(id_conta_origem)
        destino = CT.get_conta_by_id(id_conta_destino)

        if not origem or origem.status != "ATIVA":
            raise ValidacaoNegocioError("Conta de origem inválida ou inativa!")

        if not destino or destino.status != "ATIVA":
            raise ValidacaoNegocioError("Conta de destino inválida ou inativa!")

        if valor <= 0:
            raise ValidacaoNegocioError("Valor da transferência deve ser positivo")

        if origem.saldo < valor:
            raise ValidacaoNegocioError("Saldo insuficiente na conta de origem")

        novo_saldo_origem = origem.saldo - valor
        novo_saldo_destino = destino.saldo + valor

        CT.atualizar_saldo(id_conta_origem, novo_saldo_origem)
        CT.atualizar_saldo(id_conta_destino, novo_saldo_destino)

        TR.insert_transacao(
            id_conta_origem=id_conta_origem,
            id_conta_destino=id_conta_destino,
            tipo_transacao="TRANSFERENCIA",
            valor=valor,
            data_hora=datetime.now(),
            descricao=descricao
        )

        return {
            "sucesso": True,
            "novo_saldo_origem": novo_saldo_origem,
            "novo_saldo_destino": novo_saldo_destino
        }

    @staticmethod
    def encerrar_conta(id_conta: int):
        conta = CT.get_conta_by_id(id_conta)
        if not conta:
            raise ValidacaoNegocioError("Conta não encontrada!")

        if conta.status != "ATIVA":
            raise ValidacaoNegocioError("A conta já não está ativa.")

        CT.update_conta(id_conta, saldo=conta.saldo, status="ENCERRADA")

        return {"sucesso": True, "mensagem": "Conta encerrada com sucesso"}

    @staticmethod
    def reativar_conta(id_conta: int):
        conta = CT.get_conta_by_id(id_conta)
        if not conta:
            raise ValidacaoNegocioError("Conta não encontrada!")

        if conta.status != "ENCERRADA":
            raise ValidacaoNegocioError("Conta não está encerrada")

        CT.update_conta(id_conta, saldo=conta.saldo, status="ATIVA")

        return {"sucesso": True, "mensagem": "Conta reativada com sucesso"}

    @staticmethod
    def consultar_status(id_conta: int):
        conta = CT.get_conta_by_id(id_conta)
        if not conta:
            raise ValidacaoNegocioError("Conta não encontrada!")

        return {
            "id_conta": conta.id_conta,
            "numero_conta": conta.numero_conta,
            "tipo_conta": conta.tipo_conta,
            "saldo": conta.saldo,
            "status": conta.status,
            "data_abertura": conta.data_abertura,
            "id_agencia": conta.id_agencia,
            "id_cliente": conta.id_cliente
        }

    @staticmethod
    def atualizar_vencimento_corrente(id_conta: int):
        dados_cc = CC.get_by_id(id_conta)
        if not dados_cc:
            raise ValidacaoNegocioError("Conta corrente não encontrada")

        ultima_transacao = TR.get_data_ultima_transacao(id_conta)
        if ultima_transacao:
            novo_vencimento = ultima_transacao.date() + relativedelta(months=6)
        else:
            novo_vencimento = datetime.today().date() + relativedelta(months=6)

        dados_cc.data_vencimento = novo_vencimento
        CC.update(dados_cc)

        return {
            "sucesso": True,
            "novo_vencimento": novo_vencimento
        }


class ContaCorrenteService:

    @staticmethod
    def criar_conta_corrente(id_conta, id_cliente):
        score = ClienteRepository.get_score_credito(id_cliente)
        limite = auxiliares.calcular_limite_por_score(score)

        taxa_manutencao = 10.00
        data_vencimento = datetime.today().date() + relativedelta(months=6)

        conta_corrente = ContaCorrente(
            id_conta=id_conta,
            limite=limite,
            data_vencimento=data_vencimento,
            taxa_manutencao=taxa_manutencao
        )

        CC.insert(conta_corrente)


class ContaPoupancaService:

    @staticmethod
    def criar_conta_poupanca(id_conta, taxa_rendimento):
        conta_poupanca = ContaPoupanca(
            id_conta=id_conta,
            taxa_rendimento=taxa_rendimento,
            ultimo_rendimento=None
        )
        CP.insert(conta_poupanca)


class ContaInvestimentoService:

    @staticmethod
    def criar_conta_investimento(id_conta, perfil_risco, valor_minimo, taxa_rendimento_base):
        conta_investimento = ContaInvestimento(
            id_conta=id_conta,
            perfil_risco=perfil_risco,
            valor_minimo=valor_minimo,
            taxa_rendimento_base=taxa_rendimento_base
        )
        CI.insert(conta_investimento)
