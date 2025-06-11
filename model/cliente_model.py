from dataclasses import dataclass

@dataclass
class Cliente:
    id_cliente: int
    id_usuario: int
    score_credito: int
