from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Conta:
    id_conta: int
    numero_conta: str
    id_agencia: int
    saldo: float
    tipo_conta: str  # 'CORRENTE', 'POUPANCA', 'INVESTIMENTO'
    id_cliente: int
    data_abertura: date
    status: str  # 'ATIVA', 'ENCERRADA'
