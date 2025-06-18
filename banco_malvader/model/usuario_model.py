from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class Usuario:
    id_usuario: Optional[int]
    nome: str
    cpf: str
    data_nascimento: date
    telefone: str
    email: str
    tipo_usuario: str  # 'CLIENTE' ou 'FUNCIONARIO'
    senha: str  # senha já criptografada
    otp_codigo: Optional[str] = None
    otp_ativo: Optional[bool] = False
    otp_expiracao: Optional[datetime] = None

    @staticmethod
    def from_row(row: dict) -> "Usuario":
        return Usuario(
            id_usuario=row.get("id_usuario"),
            nome=row["nome"],
            cpf=row["cpf"],
            data_nascimento=row["data_nascimento"],
            telefone=row["telefone"],
            email=row["email"],
            tipo_usuario=row["tipo_usuario"],
            senha=row["senha_hash"],  # <- mapeia senha_hash -> senha
            otp_ativo=row["otp_ativo"],
            otp_codigo=row.get("otp_codigo"),
            otp_expiracao=row.get("otp_expiracao")
        )