from dataclasses import dataclass
from datetime import date

@dataclass
class ContaCorrente:
    id_conta: int
    limite: float
    data_vencimento: date
    taxa_manutencao: float
