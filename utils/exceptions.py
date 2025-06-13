
class BancoMalvaderError(Exception):
    """Exceção base para todos os erros do sistema Banco Malvader."""
    pass

class ValidacaoNegocioError(BancoMalvaderError):
    """Erro de validação de regra de negócio."""
    pass

class ClienteNaoEncontradoError(BancoMalvaderError):
    """Erro quando um cliente não é localizado."""
    pass

class AcessoNegadoError(BancoMalvaderError):
    """Erro de autenticação ou permissão."""
    def __init__(self, mensagem="Acesso negado."):
        super().__init__(mensagem)

class ContaInativaError(BancoMalvaderError):
    """Erro quando uma operação é solicitada em uma conta inativa ou encerrada."""
    pass

class TransacaoBloqueadaError(BancoMalvaderError):
    """Erro quando uma transação não pode ser realizada por regra do sistema."""
    pass

class LimiteSaquesExcedidoError(BancoMalvaderError):
    """Erro quando o cliente ultrapassa o número de saques permitido."""
    pass

class SaldoInsuficienteError(BancoMalvaderError):
    """Erro quando o saldo ou limite da conta não é suficiente para a operação."""
    pass

class UsuarioJaExisteError(BancoMalvaderError):
    """Erro quando já existe um usuário com o mesmo CPF/email."""
    pass