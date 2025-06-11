from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Usuario:
    id_usuario: Optional[int]
    nome: str
    cpf: str
    data_nascimento: datetime
    telefone: Optional[str]
    email: Optional[str]
    tipo_usuario: str  # 'CLIENTE' ou 'FUNCIONARIO'
    senha_hash: str
    otp_ativo: bool = False
    otp_expiracao: Optional[datetime] = None
