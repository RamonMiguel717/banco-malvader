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

        CC.insert_conta_corrente(id_conta, limite, data_vencimento, taxa_manutencao)

            
    @staticmethod
    def consultar_saldo(id_conta, senha, otp, id_usuario):
        try:
            if not usuario.validar_senha(id_usuario, senha):
                raise ValidacaoNegocioError("Senha inválida.")
            if not usuario.validar_otp(id_usuario, otp):
                raise ValidacaoNegocioError("OTP inválido ou expirado.")
            
            conta_info = conta.get_conta_by_id(id_conta)
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

        except Exception as e:
            raise ValidacaoNegocioError(f"Erro ao consultar saldo: {e}")

    @staticmethod
    def consultar_extrato(id_conta: int, limite: int = 50):
        try:
            extrato = conta.get_transacoes_da_conta(id_conta, limite)
            return [
                {
                    "id_transacao": trans["id_transacao"],
                    "data_hora": trans["data_hora"],
                    "tipo_transacao": trans["tipo_transacao"],
                    "valor": float(trans["valor"]),
                    "descricao": trans["descricao"],
                    "conta_origem": trans["id_conta_origem"],
                    "conta_destino": trans["id_conta_destino"]
                }
                for trans in extrato
            ]
        except Exception as e:
            raise ValidacaoNegocioError(f"Erro ao consultar extrato: {e}")

    @staticmethod
    def consultar_extrato_por_periodo(id_conta, data_inicio, data_fim):
        data_inicio = tratar_data(data_inicio)
        data_fim = tratar_data(data_fim)
        try:
            extrato = conta.get_transacoes_por_periodo(id_conta, data_inicio, data_fim)
            return [
                {
                    "id_transacao": trans["id_transacao"],
                    "data_hora": trans["data_hora"],
                    "tipo_transacao": trans["tipo_transacao"],
                    "valor": float(trans["valor"]),
                    "descricao": trans["descricao"],
                    "conta_origem": trans["id_conta_origem"],
                    "conta_destino": trans["id_conta_destino"]
                }
                for trans in extrato
            ]

        except Exception as e:
            raise ValidacaoNegocioError(f"Erro ao consultar extrato: {e}")

from datetime import datetime, timedelta

class ContaCorrente:
    
    @staticmethod
    def realizar_saque(id_conta: int, id_agencia: int, valor: float, descricao: str = "Saque"):
        """Realiza um saque na conta corrente após validar diversas condições.
        
        Args:
            id_conta: ID da conta corrente
            id_agencia: ID da agência
            valor: Valor a ser sacado
            descricao: Descrição da operação (padrão: "Saque")
            
        Raises:
            ValidacaoNegocioError: Se alguma validação falhar
        """
        # 1. Validação da conta
        conta = get_conta_by_id(id_conta)
        if not conta or conta.status != "ATIVA":
            raise ValidacaoNegocioError("Conta inválida ou inativa!")

        # 2. Validação da agência
        if conta.id_agencia != id_agencia:
            raise ValidacaoNegocioError("Conta não pertence à agência informada")

        # 3. Obter dados da conta corrente
        dados_cc = CC.get_by_id(id_conta)
        if not dados_cc:
            raise ValidacaoNegocioError("Dados da conta corrente não encontrados")

        # 4. Verificar saldo/disponibilidade
        if valor <= 0:
            raise ValidacaoNegocioError("Valor do saque deve ser positivo")
            
        if dados_cc.saldo < valor:
            raise ValidacaoNegocioError("Saldo insuficiente")

        # 5. Verificar limite de saques (últimos 30 dias)
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=30)
        transacoes = get_transacoes_por_periodo(id_conta, data_inicio, data_fim)
        
        saques_30_dias = [t for t in transacoes if t.tipo == "SAQUE"]
        if len(saques_30_dias) >= dados_cc.limite_saques:
            raise ValidacaoNegocioError("Limite de saques excedido")

        # 6. Realizar o saque
        novo_saldo = dados_cc.saldo - valor
        CC.atualizar_saldo(id_conta, novo_saldo)


        #TODO isso está errado, adicionar a função update
        registrar_transacao(
            id_conta=id_conta,
            tipo="SAQUE",
            valor=valor,
            descricao=descricao,
            data=datetime.now()
        )
        
        return {"sucesso": True, "novo_saldo": novo_saldo}