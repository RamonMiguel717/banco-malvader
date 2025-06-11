class BancoMalvaderError(Exception):
    pass

class ValidacaoNegocioError(BancoMalvaderError):
    pass

class ClienteNaoEncontradoError(BancoMalvaderError):
    pass
