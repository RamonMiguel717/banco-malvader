from dataclasses import dataclass

@dataclass
class Endereco:
    id_endereco: int
    id_usuario: int
    cep: str
    local: str
    numero_casa: int
    bairro: str
    cidade: str
    estado: str
    complemento: str | None = None
