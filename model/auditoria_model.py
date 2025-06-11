from dataclasses import dataclass
from datetime import datetime

@dataclass
class Auditoria:
    id_auditoria: int
    id_usuario: int
    acao: str
    data_hora: datetime
    detalhes: dict
