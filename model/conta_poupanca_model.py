from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class ContaPoupanca:
    id_conta: int
    taxa_rendimento: float
    ultimo_rendimento: Optional[date]
