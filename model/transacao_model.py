from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Transacao:
    id_transacao: int
    id_conta_origem: Optional[int]
    id_conta_destino: Optional[int]
    tipo_transacao: str  # 'SAQUE', 'DEPOSITO', 'TRANSFERENCIA'
    valor: float
    data_hora: datetime
    descricao: Optional[str]
