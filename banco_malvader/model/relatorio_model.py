from dataclasses import dataclass
from datetime import datetime

@dataclass
class Relatorio:
    id_relatorio: int
    id_funcionario: int
    tipo_relatorio: str
    data_geracao: datetime
    conteudo: str
