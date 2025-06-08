from utils.validator import Validator
from utils.criptografia_senha import criptografada
from repository.clienteDAO import ClienteRepository as Cliente
from repository.usuarioDAO import UsuarioRepository as usuario
from repository.contasDAO import ContaCorrenteRepository as CC, ContaInvestimentoRepository as CI, ContaPoupancaRepository as CP, ContaRepository as conta
from utils.exceptions import ValidacaoNegocioError, ClienteNaoEncontradoError

"""
As camadas SERVICES são o ultimo ponto antes do FRONT
Fazem a validação de campos e aplicam as REGRAS DE NEGÓCIO

"""


class ClienteServices:

    @staticmethod
    # Função base para a validação de campo
    def _validar_campo(label, resultado_validacao):
        if not resultado_validacao['valido']:
            raise ValidacaoNegocioError(f"{label} inválido: {resultado_validacao['erros']}")
    # Retorna um objeto de validação de negócio indicando onde foi o erro

    @staticmethod
    # Cria a conta após validar todos os campos inseridos
    def create_account(nome, cpf, data_nascimento, senha, telefone, email, tipo_usuario='CLIENTE'):
        try:
            ClienteServices._validar_campo("Nome", Validator.validate_nome(nome))
            ClienteServices._validar_campo("CPF", Validator.validate_cpf(cpf))
            ClienteServices._validar_campo("Senha", Validator.validate_senha(senha))
            ClienteServices._validar_campo("Telefone", Validator.validate_telefone(telefone))
            ClienteServices._validar_campo("Email", Validator.validate_email(email))
            ClienteServices._validar_campo("Data de nascimento", Validator.validate_idade(data_nascimento))

            # Criptografa a senha para o modelo HASK
            senha_hash = criptografada(senha)

            # Chamada de funão DAO de inserção no banco de dados
            usuario.insert_usuario(nome, cpf, data_nascimento, telefone, email, tipo_usuario, senha_hash, False, None)
            id_usuario = usuario.get_usuario_by_cpf(cpf)['id_usuario']
            Cliente.insert_cliente(id_usuario)

            # Retorna lista com as informações de resultado do cadastro
            return {"status": "sucesso", "id_usuario": id_usuario}

        except Exception as e:
            raise ValidacaoNegocioError(f"Erro ao criar conta do cliente: {e}")

    @staticmethod
    # Desempacota as informações encontradas pelo id_usuário e as exibe
    def get_cliente_by_usuario(id_usuario):
        try:
            cliente = Cliente.get_cliente_by_id(id_usuario)
            contas = conta.get_contas_by_cliente(cliente['id_cliente'])
            score = cliente['score_credito']
            return {
                'cliente': cliente,
                'contas': contas,
                'score': score
            }
        except Exception as e:
            raise ClienteNaoEncontradoError(f"Erro ao identificar cliente: {e}")

    @staticmethod
        # Desempacota as informações encontradas pelo cpf e as exibe
    def get_cliente_by_cpf(cpf):
        try:
            cliente = Cliente.get_cliente_by_cpf(cpf)
            contas = conta.get_contas_by_cliente(cliente['id_cliente'])
            score = cliente['score_credito']
            return {
                'cliente': cliente,
                'contas': contas,
                'score': score
            }
        except Exception as e:
            raise ClienteNaoEncontradoError(f"Não foi possível encontrar o cliente: {e}")

    @staticmethod
        # Desempacota as informações encontradas pelo id_cliente e as exibe
    def get_contas_do_cliente(id_cliente):
        try:
            return conta.get_contas_by_cliente(id_cliente)
        except Exception as e:
            raise ValidacaoNegocioError(f"Não foi possível encontrar as contas do cliente: {e}")

    @staticmethod
    # Lista os clientes em uma formatação especifica
    def list_clientes():
        try:
            clientes_cru = Cliente.listar_clientes_completo()
            return [
                {
                    "id_cliente": cliente["id_cliente"],
                    "nome": cliente["nome"],
                    "cpf": cliente["cpf"],
                    "score_credito": cliente["score_credito"]
                }
                for cliente in clientes_cru
            ]
        except Exception as e:
            raise ValidacaoNegocioError(f"Não foi possível listar os clientes: {e}")
    
    

    @staticmethod
    # Recalcula o score do cliente 
    def recalcular_score(id_cliente):
        try:
            Cliente.recalcular_score_credito(id_cliente)
            return {"status": "score recalculado com sucesso"}
        except Exception as e:
            raise ValidacaoNegocioError(f"Erro ao recalcular score: {e}")

    #TODO criar uma função para atualizar o SCORE do cliente

    @staticmethod
    def excluir_cliente(id_cliente):
        try:
            Cliente.delete_cliente(id_cliente)
            return {"status": "cliente excluído com sucesso"}
        except Exception as e:
            raise ValidacaoNegocioError(f"Erro ao excluir cliente: {e}")
        
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
    def consultar_status_limite(id_cliente):
        try:
            contas_cliente = conta.get_contas_by_cliente(id_cliente)
            return [
                {
                    "numero_conta": c["numero_conta"],
                    "tipo_conta": c["tipo_conta"],
                    "status": c["status"],
                    "limite": c.get("limite", 0.0),
                    "saldo": c["saldo"]
                }
                for c in contas_cliente
            ]
        except Exception as e:
            raise ValidacaoNegocioError(f"Erro ao consultar status/limite: {e}")


