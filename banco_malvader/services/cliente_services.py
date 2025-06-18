from banco_malvader.utils.validator import Validator
from banco_malvader.model.cliente_model import Cliente as client
from banco_malvader.model.usuario_model import Usuario
from banco_malvader.utils.criptografia_senha import criptografada
from banco_malvader.repository.cliente_dao import ClienteRepository as Cliente
from banco_malvader.repository.usuario_dao import UsuarioRepository as usuario
from banco_malvader.repository.contas_dao import ContaCorrenteRepository as CC, ContaInvestimentoRepository as CI, ContaPoupancaRepository as CP, ContaRepository as conta
from banco_malvader.utils.exceptions import ValidacaoNegocioError, ClienteNaoEncontradoError

class ClienteServices:

    @staticmethod
    def _validar_campo(label, resultado_validacao):
        if not resultado_validacao['valido']:
            raise ValidacaoNegocioError(f"{label} inválido: {resultado_validacao['erros']}")

    @staticmethod
    def create_account(nome, cpf, data_nascimento, senha, telefone, email, tipo_usuario='CLIENTE'):
        try:
            # Validações
            ClienteServices._validar_campo("Nome", Validator.validate_nome(nome))
            ClienteServices._validar_campo("CPF", Validator.validate_cpf(cpf))
            ClienteServices._validar_campo("Senha", Validator.validate_senha(senha, email, nome))
            ClienteServices._validar_campo("Telefone", Validator.validate_telefone(telefone))
            ClienteServices._validar_campo("Email", Validator.validate_email(email))
            ClienteServices._validar_campo("Data de nascimento", Validator.validate_idade(data_nascimento))

            senha_hash = criptografada.criptografar_senha(senha)

            # Cria objeto Usuario
            usuario_obj = Usuario(
                id_usuario=None,
                nome=nome,
                cpf=cpf,
                data_nascimento=data_nascimento,
                telefone=telefone,
                email=email,
                tipo_usuario=tipo_usuario,
                senha=senha_hash,
                otp_ativo=False,
                otp_codigo=None,
                otp_expiracao=None
            )

            # Insere no banco e retorna o id gerado
            id_usuario = usuario.insert_usuario(usuario_obj)

            # Cria objeto Cliente
            cliente_obj = client(
                id_cliente=None,
                id_usuario=id_usuario,
                score_credito=0
            )

            Cliente.insert_cliente(cliente_obj)

            return {"status": "sucesso", "id_usuario": id_usuario}

        except Exception as e:
            raise ValidacaoNegocioError(f"Erro ao criar conta do cliente: {e}")
    @staticmethod
    def get_cliente_by_usuario(id_usuario):
        try:
            cliente = Cliente.get_cliente_by_id(id_usuario)
            contas = conta.get_contas_by_cliente(cliente.id_cliente)
            return {
                'cliente': cliente,
                'contas': contas,
                'score': cliente.score_credito
            }
        except Exception as e:
            raise ClienteNaoEncontradoError(f"Erro ao identificar cliente: {e}")

    @staticmethod
    def get_cliente_by_cpf(cpf):
        try:
            cliente = Cliente.get_cliente_by_cpf(cpf)
            contas = conta.get_contas_by_cliente(cliente.id_cliente)
            return {
                'cliente': cliente,
                'contas': contas,
                'score': cliente.score_credito
            }
        except Exception as e:
            raise ClienteNaoEncontradoError(f"Não foi possível encontrar o cliente: {e}")

    @staticmethod
    def get_contas_do_cliente(id_cliente):
        try:
            return conta.get_contas_by_cliente(id_cliente)
        except Exception as e:
            raise ValidacaoNegocioError(f"Não foi possível encontrar as contas do cliente: {e}")

    @staticmethod
    def list_clientes():
        try:
            clientes_cru = Cliente.listar_clientes_completo()
            return [
                {
                    "id_cliente": cliente.id_cliente,
                    "nome": cliente.nome,
                    "cpf": cliente.cpf,
                    "score_credito": cliente.score_credito
                }
                for cliente in clientes_cru
            ]
        except Exception as e:
            raise ValidacaoNegocioError(f"Não foi possível listar os clientes: {e}")

    @staticmethod
    def recalcular_score(id_cliente):
        try:
            Cliente.recalcular_score_credito(id_cliente)
            return {"status": "score recalculado com sucesso"}
        except Exception as e:
            raise ValidacaoNegocioError(f"Erro ao recalcular score: {e}")

    @staticmethod
    def excluir_cliente(id_cliente):
        try:
            Cliente.delete_cliente(id_cliente)
            return {"status": "cliente excluído com sucesso"}
        except Exception as e:
            raise ValidacaoNegocioError(f"Erro ao excluir cliente: {e}")

    @staticmethod
    def consultar_status_limite(id_cliente):
        try:
            contas_cliente = conta.get_contas_by_cliente(id_cliente)
            return [
                {
                    "numero_conta": c.numero_conta,
                    "tipo_conta": c.tipo_conta,
                    "status": c.status,
                    "limite": getattr(c, "limite", 0.0),
                    "saldo": c.saldo
                }
                for c in contas_cliente
            ]
        except Exception as e:
            raise ValidacaoNegocioError(f"Erro ao consultar status/limite: {e}")