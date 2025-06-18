from dataclasses import dataclass
from typing import Optional

@dataclass
class Funcionario:
    id_funcionario: int
    id_usuario: int
    codigo_funcionario: str
    cargo: str  # 'ESTAGIARIO', 'ATENDENTE', 'GERENTE'
    id_supervisor: Optional[int] = None
